#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UserPromptSubmit Hook for za-qe plugin.
Provides slash command context injection and skills activation strategy.

@author Alfie
"""
import json
import sys
import re
import io

# 设置编码
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ==== 配置常量 ====
CONFIG = {
    'commands': {
        'no_enhancement': [
            'qe-status', 'qe-help', 'qe-config',
            'za-qe:qe-status', 'za-qe:qe-help', 'za-qe:qe-config'
        ],
        'deep_enhancement': [
            'qe-quick', 'manual-case', 'full-workflow', 'req-parser',
            'za-qe:qe-quick', 'za-qe:manual-case', 'za-qe:full-workflow', 'za-qe:req-parser'
        ],
    }
}


def render_template(template_key: str, **kwargs) -> str:
    """渲染模板"""
    cmd = kwargs.get('command', '')
    templates = {
        'unified_deep_intent_analysis': (
            f"""执行 `/{cmd}` 前完成意图分析：
1. 意图解析：用户的真实需求是什么？输入文档类型？期望输出？
2. 风险预判：文档格式是否兼容？是否需要补充信息？
3. 执行前声明：「我理解您需要：xxx；我将会：xxx」

严守输入文档边界，不添加用户未要求的内容。"""
        ),
    }
    return templates.get(template_key, '')


try:
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    prompt = input_data.get("prompt", "")
    cwd = input_data.get("cwd", "")

    def detect_slash_command_context(prompt_text: str) -> str:
        """检测slash command相关的上下文"""
        trimmed_prompt = prompt_text.strip()
        slash_match = re.search(r'^/([a-zA-Z][a-zA-Z0-9_:-]*)', trimmed_prompt)

        if not slash_match:
            return ""

        command = slash_match.group(1)

        # 无增强命令直接跳过
        if any(cmd in command for cmd in CONFIG['commands']['no_enhancement']):
            return ""

        # 深度增强命令
        if any(cmd in command for cmd in CONFIG['commands']['deep_enhancement']):
            return render_template('unified_deep_intent_analysis', command=command)

        return ""

    def should_activate_skills(prompt_text: str) -> bool:
        """判断是否需要激活Skills策略

        斜杠命令不激活（命令内部会自己处理）
        自然语言暂不激活
        """
        trimmed_prompt = prompt_text.strip()
        if re.match(r'^/', trimmed_prompt):
            return False
        return False

    def get_skills_activation_strategy() -> str:
        """返回Skills激活策略说明"""
        return """
<system-rules>
🔧 Skills激活判断规则：
- ✅ 必须激活：用户消息涉及测试用例生成、接口分析、需求文档分析、测试左移等
- ❌ 不激活：① 工作流中的问答 ② 纯问候
- 激活方式：读取 `.claude/skills/skills.json`，匹配最相关的 1-3 个 skill 并调用
</system-rules>"""

    # 检测slash command上下文
    slash_context = detect_slash_command_context(prompt)

    # 智能Skills激活策略（仅在需要时激活）
    skills_strategy = ""
    if should_activate_skills(prompt):
        skills_strategy = get_skills_activation_strategy()

    base_context = """{0}
所有交互使用中文，技术术语和代码除外。输出内容善用换行和列表，避免流水账。
""".format(skills_strategy)

    full_context = base_context + slash_context

    # Output via hookSpecificOutput format
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": full_context,
        },
    }))

    sys.exit(0)

except Exception as e:
    # 发生任何异常时，输出空JSON并静默退出，不影响正常流程
    print(json.dumps({}), file=sys.stderr)
    sys.exit(1)

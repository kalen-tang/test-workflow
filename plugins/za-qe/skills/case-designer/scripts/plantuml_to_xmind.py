#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "md2xmind>=1.0.0",
# ]
# ///
"""
从 Markdown 场景案例文件中提取详细测试案例 PlantUML，转换为 XMind 文件。

用法:
    uv run plantuml_to_xmind.py <markdown_file> <requirement_id>

参数:
    markdown_file: 场景案例 Markdown 文件路径（包含 PlantUML 代码块）
    requirement_id: 需求ID（如 BANK-1234），用作输出文件名

示例:
    uv run plantuml_to_xmind.py ./result/xxx_场景案例.md BANK-1234
    # 输出: ./result/BANK-1234_CASE.xmind
"""

import io
import pathlib
import re
import sys

import md2xmind


def extract_test_case_mindmap(md_content: str) -> str:
    """
    从 Markdown 内容中提取"详细测试案例"部分的 PlantUML MindMap 代码块。

    :param md_content: Markdown 文件内容
    :return: PlantUML MindMap 内容（@startmindmap...@endmindmap）
    :raises ValueError: 找不到测试案例部分或 PlantUML 代码块
    """
    # 找到"详细测试案例"标题后的第一个 plantuml 代码块
    pattern = re.compile(
        r'##\s*详细测试案例.*?```plantuml\s*\n(@startmindmap.*?@endmindmap)\s*\n```',
        re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(md_content)
    if match:
        return match.group(1)

    # 兼容：没有"详细测试案例"标题，取最后一个 @startmindmap 块
    blocks = re.findall(r'(@startmindmap.*?@endmindmap)', md_content, re.DOTALL)
    if blocks:
        return blocks[-1]

    raise ValueError("找不到测试案例 PlantUML 代码块，请确认 Markdown 文件包含 '详细测试案例' 部分")


def plantuml_to_md(plantuml_content: str) -> str:
    """
    将 PlantUML MindMap 内容转换为 md2xmind 需要的 Markdown 格式（* 替换为 #）。

    :param plantuml_content: PlantUML MindMap 内容
    :return: Markdown 格式内容
    """
    start = plantuml_content.find("\n* ")
    end = plantuml_content.find("\n@endmindmap")
    if start == -1 or end == -1:
        raise ValueError("无效的 PlantUML MindMap 格式：找不到节点内容")

    md_content = plantuml_content[start:end]
    # 替换 * 为 # 但跳过 right side / left side 指令行
    lines = []
    for line in md_content.splitlines():
        stripped = line.strip()
        if stripped in ("right side", "left side"):
            continue
        lines.append(line.replace("*", "#"))
    return "\n".join(lines).strip()


def convert(markdown_file: str, requirement_id: str) -> str:
    """
    从 Markdown 文件中提取测试案例 MindMap 并转换为 XMind。

    :param markdown_file: Markdown 文件路径
    :param requirement_id: 需求ID
    :return: 输出的 XMind 文件路径
    """
    md_path = pathlib.Path(markdown_file)
    if not md_path.exists():
        raise FileNotFoundError(f"文件不存在: {markdown_file}")

    md_content = md_path.read_text(encoding="utf-8")
    plantuml_content = extract_test_case_mindmap(md_content)
    md_for_xmind = plantuml_to_md(plantuml_content)

    output_file = md_path.parent / f"{requirement_id}_CASE.xmind"

    # 屏蔽 md2xmind 库自身的 print 输出（含乱码）
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        md2xmind.start_trans_content(md_for_xmind, str(output_file), "测试案例")
    finally:
        sys.stdout = old_stdout

    return str(output_file)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    markdown_file = sys.argv[1]
    requirement_id = sys.argv[2]

    try:
        output_path = convert(markdown_file, requirement_id)
        print(f"OK: {output_path}")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

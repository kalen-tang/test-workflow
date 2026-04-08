#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "md2xmind>=1.0.0",
# ]
# ///
"""
PlantUML MindMap 转 XMind 工具

从 PlantUML mindmap 格式转换为 XMind 格式文件。

用法:
    uv run plantuml_to_xmind.py <plantuml_file> <requirement_id>

参数:
    plantuml_file: PlantUML 文件路径（包含 @startmindmap...@endmindmap）
    requirement_id: 需求ID（如 BANK-1234），用作输出文件名

示例:
    uv run plantuml_to_xmind.py ./result/test-cases.puml BANK-1234
    # 输出: ./result/BANK-1234.xmind
"""

import pathlib
import sys

import md2xmind


def plantuml_to_xmind(plantuml_file: str, requirement_id: str) -> str:
    """
    将 PlantUML mindmap 转换为 XMind 文件。

    :param plantuml_file: PlantUML 文件路径
    :param requirement_id: 需求ID（如 BANK-1234）
    :return: 生成的 XMind 文件路径
    """
    # 读取 PlantUML 文件内容
    plantuml_path = pathlib.Path(plantuml_file)
    if not plantuml_path.exists():
        raise FileNotFoundError(f"PlantUML 文件不存在: {plantuml_file}")

    plantuml_content = plantuml_path.read_text(encoding="utf-8")

    # 提取 mindmap 内容（@startmindmap 到 @endmindmap 之间）
    start_index = plantuml_content.find("\n* ")
    end_index = plantuml_content.find("\n@endmindmap")

    if start_index == -1 or end_index == -1:
        raise ValueError("无效的 PlantUML mindmap 格式：找不到 '* ' 或 '@endmindmap'")

    # 提取并转换为 Markdown 格式（md2xmind 需要 # 开头）
    md_content = plantuml_content[start_index:end_index]
    md_content = md_content.replace("*", "#").strip()

    # 输出到同目录，文件名为需求ID
    output_dir = plantuml_path.parent
    output_file = output_dir / f"{requirement_id}.xmind"

    # 转换为 XMind
    md2xmind.start_trans_content(md_content, str(output_file), "测试案例")

    return str(output_file.relative_to("."))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    plantuml_file = sys.argv[1]
    requirement_id = sys.argv[2]

    try:
        output_path = plantuml_to_xmind(plantuml_file, requirement_id)
        print(f"✅ XMind 文件已生成: {output_path}")
    except Exception as e:
        print(f"❌ 转换失败: {e}", file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.27.0",
# ]
# ///
"""
验证 PlantUML 代码是否有语法错误，通过请求 plantuml.in.za 渲染服务检测。

用法：
    uv run validate_plantuml.py <plantuml_code>
    uv run validate_plantuml.py --file <md_or_puml_file>

输出（每个代码块一行）：
    OK: <index> <url>          → 验证通过，附渲染 URL
    ERROR: <index> <message>   → 语法错误，附错误描述

退出码：
    0 → 全部通过
    1 → 存在语法错误
"""

import re
import sys
import zlib
import string
import httpx

PLANTUML_SERVER = "https://plantuml.in.za/svg"

# PlantUML 使用的自定义 base64 字符表
_PLANTUML_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
_STD_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
_TO_PLANTUML = str.maketrans(_STD_CHARS, _PLANTUML_CHARS)
_FROM_PLANTUML = str.maketrans(_PLANTUML_CHARS, _STD_CHARS)


def encode_plantuml(source: str) -> str:
    """将 PlantUML 源码编码为 URL 路径段。"""
    compressed = zlib.compress(source.encode("utf-8"), 9)[2:-4]
    import base64
    b64 = base64.b64encode(compressed).decode("ascii")
    return b64.translate(_TO_PLANTUML)


def extract_blocks(text: str) -> list[str]:
    """从文本中提取所有 PlantUML 代码块（@startuml/@startmindmap/@startwbs 等）。"""
    # 匹配 markdown 代码块内的 plantuml 内容
    md_pattern = re.compile(
        r"```(?:plantuml)?\s*\n(@start\w+.*?@end\w+)\s*\n```",
        re.DOTALL | re.IGNORECASE,
    )
    blocks = md_pattern.findall(text)
    if blocks:
        return blocks

    # 直接包含 @start 标记的纯文本
    raw_pattern = re.compile(
        r"(@start\w+.*?@end\w+)",
        re.DOTALL | re.IGNORECASE,
    )
    return raw_pattern.findall(text)


def validate_block(source: str, index: int) -> tuple[bool, str]:
    """
    验证单个 PlantUML 代码块。
    返回 (ok, message)：ok=True 表示通过，message 含 URL 或错误信息。
    """
    encoded = encode_plantuml(source)
    url = f"{PLANTUML_SERVER}/{encoded}"

    try:
        resp = httpx.get(url, timeout=15, follow_redirects=True)
    except httpx.RequestError as e:
        return False, f"网络请求失败: {e}"

    if resp.status_code != 200:
        return False, f"HTTP {resp.status_code}"

    svg = resp.text

    # 错误判断：SVG 中含 "Syntax Error?" 文字
    if "Syntax Error?" in svg:
        # 从错误 SVG 中提取错误描述
        error_match = re.search(
            r"Syntax Error\?[^<]*\(([^)]+)\)",
            svg,
        )
        error_detail = error_match.group(1) if error_match else "语法错误（详见渲染结果）"
        return False, f"{error_detail} → {url}"

    return True, url


def main() -> int:
    args = sys.argv[1:]

    if not args:
        print("用法: validate_plantuml.py <plantuml_code 或 --file <文件路径>>", file=sys.stderr)
        return 2

    if args[0] == "--file":
        if len(args) < 2:
            print("错误: --file 需要指定文件路径", file=sys.stderr)
            return 2
        path = args[1]
        try:
            text = open(path, encoding="utf-8").read()
        except OSError as e:
            print(f"错误: 无法读取文件 {path}: {e}", file=sys.stderr)
            return 2
        blocks = extract_blocks(text)
        if not blocks:
            print("未找到任何 PlantUML 代码块", file=sys.stderr)
            return 2
    else:
        # 直接传入 PlantUML 代码
        blocks = [" ".join(args)]

    has_error = False
    for i, block in enumerate(blocks, start=1):
        ok, msg = validate_block(block.strip(), i)
        if ok:
            print(f"OK: {i} {msg}")
        else:
            print(f"ERROR: {i} {msg}")
            has_error = True

    return 1 if has_error else 0


if __name__ == "__main__":
    sys.exit(main())

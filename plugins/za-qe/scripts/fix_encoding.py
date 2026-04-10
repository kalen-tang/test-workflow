#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
检查并修复文本文件的编码，确保输出为 UTF-8。

用法:
    uv run fix_encoding.py <file_path> [file_path2 ...]

输出:
    OK: <path>          - 文件已是有效 UTF-8
    FIXED: <path> from <enc>  - 已从 enc 转换为 UTF-8
    WARN: <path>        - 无法识别编码，需人工检查
    ERROR: <path> <msg> - 文件读取失败
"""

import sys
import pathlib

ENCODINGS = ["utf-8-sig", "gb18030", "big5", "utf-16"]


def fix_encoding(path: str) -> None:
    p = pathlib.Path(path)
    try:
        raw = p.read_bytes()
    except OSError as e:
        print(f"ERROR: {path} {e}", file=sys.stderr)
        return

    try:
        raw.decode("utf-8")
        print(f"OK: {path}")
        return
    except UnicodeDecodeError:
        pass

    for enc in ENCODINGS:
        try:
            text = raw.decode(enc)
            p.write_text(text, encoding="utf-8")
            print(f"FIXED: {path} from {enc}")
            return
        except (UnicodeDecodeError, UnicodeError):
            continue

    print(f"WARN: {path} encoding unknown, may need manual check")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    for file_path in sys.argv[1:]:
        fix_encoding(file_path)

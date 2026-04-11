#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "markitdown[docx]>=0.1.0",
# ]
# ///
"""
将目录中的 docx/doc 文件转换为 UTF-8 Markdown。

用法:
    uv run convert_docx.py <input_dir> <output_dir> [--prefix PREFIX]

参数:
    input_dir:   包含 .docx/.doc 文件的目录
    output_dir:  Markdown 输出目录（不存在时自动创建）
    --prefix:    输出文件名前缀（可选，如 "design_"）

输出格式:
    OK:    <output_path>           转换并确认为 UTF-8
    FIXED: <output_path> from <enc> 转换后修复了编码
    WARN:  <output_path>           编码无法识别，需人工检查
    ERROR: <input_path> <message>  转换失败

示例:
    uv run convert_docx.py D:/docs/req D:/result
    uv run convert_docx.py D:/docs/design D:/result --prefix design_
"""

import argparse
import pathlib
import sys

from markitdown import MarkItDown

ENCODINGS = ["utf-8-sig", "gb18030", "big5", "utf-16"]


def fix_encoding(path: pathlib.Path) -> str:
    """检查并修复文件编码，确保为 UTF-8。返回 'ok'、'fixed:<enc>' 或 'warn'。"""
    raw = path.read_bytes()
    try:
        raw.decode("utf-8")
        return "ok"
    except UnicodeDecodeError:
        pass
    for enc in ENCODINGS:
        try:
            text = raw.decode(enc)
            path.write_text(text, encoding="utf-8")
            return f"fixed:{enc}"
        except (UnicodeDecodeError, UnicodeError):
            continue
    return "warn"


def convert(input_dir: str, output_dir: str, prefix: str = "") -> int:
    """
    扫描 input_dir 中的 docx/doc 文件，转换为 Markdown 并修复编码。

    :return: 失败文件数
    """
    src = pathlib.Path(input_dir)
    dst = pathlib.Path(output_dir)
    dst.mkdir(parents=True, exist_ok=True)

    files = sorted(list(src.glob("*.docx")) + list(src.glob("*.doc")))
    if not files:
        print(f"WARN: no docx/doc files found in {input_dir}", file=sys.stderr)
        return 0

    md = MarkItDown()
    errors = 0

    for f in files:
        out = dst / f"{prefix}{f.stem}.md"
        try:
            result = md.convert(str(f))
            out.write_text(result.text_content, encoding="utf-8")
        except Exception as e:
            print(f"ERROR: {f} {e}", file=sys.stderr)
            errors += 1
            continue

        status = fix_encoding(out)
        if status == "ok":
            print(f"OK: {out}")
        elif status.startswith("fixed:"):
            enc = status.split(":", 1)[1]
            print(f"FIXED: {out} from {enc}")
        else:
            print(f"WARN: {out}")

    return errors


if __name__ == "__main__":
    import io
    import os

    # Windows 终端默认 GBK，Python stdout 默认 UTF-8 会导致中文路径乱码
    # Linux/Mac 通常是 UTF-8 无需处理
    if os.name == "nt" and hasattr(sys.stdout, "buffer"):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=sys.getdefaultencoding(), errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding=sys.getdefaultencoding(), errors="replace")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input_dir", help="包含 docx/doc 文件的输入目录")
    parser.add_argument("output_dir", help="Markdown 输出目录")
    parser.add_argument("--prefix", default="", help="输出文件名前缀（如 design_）")
    args = parser.parse_args()

    errors = convert(args.input_dir, args.output_dir, args.prefix)
    sys.exit(1 if errors else 0)

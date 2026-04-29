#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "markitdown[docx]>=0.1.0",
#     "chardet>=5.0",
# ]
# ///
"""
将 docx/doc 文件转换为 UTF-8 Markdown。支持批量（目录模式）和单文件模式。

用法:
    # 批量模式：转换目录中所有 docx/doc
    uv run convert_docx.py <input_dir> <output_dir> [--prefix PREFIX]

    # 单文件模式：转换单个文件到指定输出路径
    uv run convert_docx.py --file <input_file> --output-file <output_path>

参数:
    input_dir:     包含 .docx/.doc 文件的目录（批量模式）
    output_dir:    Markdown 输出目录（批量模式，不存在时自动创建）
    --prefix:      输出文件名前缀（批量模式可选，如 "design_"）
    --file:        单个 docx/doc 文件路径（单文件模式）
    --output-file: 输出 Markdown 文件完整路径（单文件模式）

输出格式:
    OK:    <output_path>           转换并确认为 UTF-8
    FIXED: <output_path> from <enc> 转换后修复了编码
    WARN:  <output_path>           编码无法识别，需人工检查
    ERROR: <input_path> <message>  转换失败

示例:
    uv run convert_docx.py D:/docs/req D:/result
    uv run convert_docx.py D:/docs/design D:/result --prefix design_
    uv run convert_docx.py --file D:/docs/需求.docx --output-file D:/project/BANK-90819_PRD.md
"""

import argparse
import pathlib
import sys

import chardet
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

    # 先用 chardet 检测编码
    detected = chardet.detect(raw)
    det_enc = detected.get("encoding")
    if det_enc:
        try:
            text = raw.decode(det_enc)
            path.write_text(text, encoding="utf-8")
            return f"fixed:{det_enc}"
        except (UnicodeDecodeError, UnicodeError, LookupError):
            pass

    # chardet 失败时回退到手动尝试
    for enc in ENCODINGS:
        try:
            text = raw.decode(enc)
            path.write_text(text, encoding="utf-8")
            return f"fixed:{enc}"
        except (UnicodeDecodeError, UnicodeError):
            continue
    return "warn"


def convert_single(input_file: str, output_file: str) -> int:
    """
    转换单个 docx/doc 文件到指定输出路径。

    :return: 0 成功，1 失败
    """
    src = pathlib.Path(input_file)
    out = pathlib.Path(output_file)
    out.parent.mkdir(parents=True, exist_ok=True)

    md = MarkItDown()
    try:
        result = md.convert(str(src))
        out.write_text(result.text_content, encoding="utf-8")
    except Exception as e:
        print(f"ERROR: {src} {e}", file=sys.stderr)
        return 1

    status = fix_encoding(out)
    if status == "ok":
        print(f"OK: {out}")
    elif status.startswith("fixed:"):
        enc = status.split(":", 1)[1]
        print(f"FIXED: {out} from {enc}")
    else:
        print(f"WARN: {out}")
    return 0


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
    parser.add_argument("input_dir", nargs="?", help="包含 docx/doc 文件的输入目录（批量模式）")
    parser.add_argument("output_dir", nargs="?", help="Markdown 输出目录（批量模式）")
    parser.add_argument("--prefix", default="", help="输出文件名前缀（如 design_）")
    parser.add_argument("--file", dest="input_file", help="单个 docx/doc 文件路径（单文件模式）")
    parser.add_argument("--output-file", dest="output_file", help="输出 Markdown 文件完整路径（单文件模式）")
    args = parser.parse_args()

    if args.input_file:
        if not args.output_file:
            parser.error("--file 需要搭配 --output-file 使用")
        errors = convert_single(args.input_file, args.output_file)
    elif args.input_dir and args.output_dir:
        errors = convert(args.input_dir, args.output_dir, args.prefix)
    else:
        parser.error("请使用批量模式（input_dir output_dir）或单文件模式（--file --output-file）")

    sys.exit(1 if errors else 0)

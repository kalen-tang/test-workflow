# .docx 文档读取脚本

用于从 `.docx` 文件一次性提取全部段落文本、表格数据和嵌入图片，供后续分析使用。

## 第一步：提取文字和表格

将 `YOUR_DOC_PATH` 和 `YOUR_REQ_ID` 替换为实际值后运行：

```bash
python -c "
import zipfile, re, os

doc_path = 'YOUR_DOC_PATH'
req_id   = 'YOUR_REQ_ID'
out_path = 'result/_tmp_docx.txt'
os.makedirs('result', exist_ok=True)

with zipfile.ZipFile(doc_path, 'r') as z:
    with z.open('word/document.xml') as f:
        content = f.read().decode('utf-8')

# 提取段落文本（记录图片占位符位置）
paragraphs = []
para_list = re.findall(r'<w:p\b[^>]*>.*?</w:p>', content, re.DOTALL)
for para in para_list:
    imgs = re.findall(r'r:embed=\"(rId\d+)\"', para)
    texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', para)
    line = ''.join(texts).strip()
    if imgs:
        paragraphs.append(f'[IMAGE:{','.join(imgs)}]')
    elif line:
        paragraphs.append(line)

# 提取表格
tables = []
for tbl in re.findall(r'<w:tbl>(.*?)</w:tbl>', content, re.DOTALL):
    rows = []
    for row in re.findall(r'<w:tr\b[^>]*>(.*?)</w:tr>', tbl, re.DOTALL):
        cells = []
        for cell in re.findall(r'<w:tc\b[^>]*>(.*?)</w:tc>', row, re.DOTALL):
            texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', cell)
            cells.append(''.join(texts).strip())
        rows.append(cells)
    tables.append(rows)

with open(out_path, 'w', encoding='utf-8') as f:
    f.write('=== 段落文本 ===\n')
    for p in paragraphs:
        f.write(p + '\n')
    f.write('\n=== 表格数据 ===\n')
    for i, t in enumerate(tables):
        f.write(f'\n[Table {i+1}]\n')
        for row in t:
            f.write(' | '.join(row) + '\n')
print('提取完成，共', len(paragraphs), '段落，', len(tables), '个表格')
"
```

运行后用 Read 工具读取 `result/_tmp_docx.txt`，其中 `[IMAGE:rIdN]` 标记表示该位置有嵌入图片。

## 第二步：提取嵌入图片

若文字提取结果中出现 `[IMAGE:rIdN]` 标记，必须运行以下脚本提取图片，并记录每张图片对应的 rId 和文件名：

```bash
python -c "
import zipfile, re, os

doc_path = 'YOUR_DOC_PATH'
req_id   = 'YOUR_REQ_ID'
img_dir  = f'result/{req_id}_images'
os.makedirs(img_dir, exist_ok=True)

with zipfile.ZipFile(doc_path, 'r') as z:
    # 读取 rId -> 文件名 映射
    with z.open('word/_rels/document.xml.rels') as f:
        rels = f.read().decode('utf-8')
    rid_map = dict(re.findall(r'Id=\"(rId\d+)\"[^>]*Target=\"media/([^\"]+)\"', rels))

    # 提取所有图片
    for rid, fname in rid_map.items():
        data = z.read(f'word/media/{fname}')
        out = f'{img_dir}/{fname}'
        with open(out, 'wb') as f:
            f.write(data)
        print(f'{rid} -> {out} ({len(data)} bytes)')
"
```

## 第三步：确认图片位置并写入规范化文档

结合 `_tmp_docx.txt` 中 `[IMAGE:rIdN]` 的前后段落文字，判断每张图片所属章节，然后：

1. 用 Read 工具逐一查看图片内容，理解图片含义
2. 在规范化 MD 中对应章节插入图片引用：

```markdown
![图片描述](YOUR_REQ_ID_images/imageN.png)
```

> ⚠️ 若图片为流程图，同时在图片下方用文字简要描述流程步骤，方便 api-generator 理解业务逻辑。

## 第四步：清理临时文件

分析完成后删除临时文件：

```bash
rm result/_tmp_docx.txt
```

> 图片文件保留在 `result/YOUR_REQ_ID_images/` 目录，供规范化 MD 引用。

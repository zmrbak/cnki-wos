"""
从 Word 论文中提取参考文献名称，保存为纯文本列表（无序号）。

支持两种参考文献格式：
  格式A（WOS/知网导出格式）：作者. 年份. 标题[类型]. 出处.
  格式B（中文期刊投稿格式）：[N] 作者. 标题[类型]. 出处, 年份.

用法:
    python extract_refs.py <docx文件路径> [-o 输出文件]
    python extract_refs.py paper.docx
    python extract_refs.py paper.docx -o result.txt
    python extract_refs.py                          # 不指定路径则提示输入
"""

import re
import sys
from pathlib import Path


# 参考文献类型标识符
REF_TYPE_PATTERN = re.compile(r'\[([A-Z]+(?:/OL)?)\]')


def extract_title(ref_text: str) -> str | None:
    """
    从一条参考文献中提取文献名称（标题）。
    优先尝试「年份前置」格式，失败则回退到通用「. 」分隔格式。
    """
    # 去掉开头的编号 [1]、[2] 等
    text = re.sub(r'^\[\d+\]\s*', '', ref_text.strip())

    # 查找文献类型标识符（如 [J]、[J/OL]、[EB/OL] 等）
    m = REF_TYPE_PATTERN.search(text)
    if not m:
        return None
    type_pos = m.start()

    prefix = text[:type_pos]

    # ---- 方法1：年份前置格式 (WOS/知网导出) ----
    # 匹配最后的 "YYYY. "，以此作为作者信息与标题的分界
    year_matches = list(re.finditer(r'\.\s+(\d{4})\.\s+', prefix))
    if year_matches:
        title_start = year_matches[-1].end()
        title = text[title_start:type_pos].strip()
        if title:
            return title.rstrip('.,; ')

    # ---- 方法2：通用 ". " 分隔格式 (中文期刊投稿) ----
    # 从类型标识符往前找最后一个 ". "（作者与标题的分隔符）
    sep_pos = prefix.rfind('. ')
    if sep_pos != -1:
        title = text[sep_pos + 2:type_pos].strip()
        if title:
            return title.rstrip('.,; ')

    return None


def extract_refs_from_docx(docx_path: Path) -> list[str]:
    """从 docx 文件中提取所有参考文献标题。"""
    try:
        from docx import Document
    except ImportError:
        print("错误: 请先安装 python-docx: pip install python-docx")
        sys.exit(1)

    doc = Document(str(docx_path))

    titles = []
    in_refs = False

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        if re.match(r'^参考文献\s*[：:]?\s*$', text):
            in_refs = True
            continue

        if in_refs:
            title = extract_title(text)
            if title:
                titles.append(title)

    return titles


def main():
    import argparse

    parser = argparse.ArgumentParser(description='从 docx 论文中提取参考文献名称')
    parser.add_argument('docx', nargs='?', help='Word 文件路径')
    parser.add_argument('-o', '--output', default=None, help='输出文件名，默认 ckwx.txt（与 Word 同目录）')
    args = parser.parse_args()

    docx_path = args.docx
    if not docx_path:
        docx_path = input("请输入Word文件路径: ").strip().strip('"')

    docx_path = Path(docx_path)
    if not docx_path.exists():
        print(f"错误: 文件不存在 - {docx_path}")
        sys.exit(1)

    if docx_path.suffix.lower() != '.docx':
        print("警告: 文件扩展名不是 .docx，可能无法正确读取")

    print(f"正在读取: {docx_path}")

    titles = extract_refs_from_docx(docx_path)

    if not titles:
        print('未找到任何参考文献，请确认文件中包含\u201c参考文献\u201d标题及条目。')
        sys.exit(0)

    # 输出文件
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = docx_path.parent / 'ckwx.txt'

    with open(output_path, 'w', encoding='utf-8') as f:
        for title in titles:
            f.write(title + '\n')

    print(f"\n已提取 {len(titles)} 条文献名称，保存至: {output_path}")
    print("-" * 50)
    for title in titles:
        print(f"  {title}")


if __name__ == '__main__':
    main()

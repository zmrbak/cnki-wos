"""
根据 ckwx.txt 中的文献名称，从 merged 开头的两个源文件中提取匹配记录
输出: ck1.txt (CNKI文献, 来自 .txt) 和 ck2.csv (WOS文献, 来自 .csv)，均不带序号前缀
用法: python extract_refs.py
"""

import os
import re
import csv
import glob

# ===== 路径配置 =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 脚本所在目录（即运行目录）
CKWX_FILE = os.path.join(BASE_DIR, 'ckwx.txt')           # 目标文献名列表（指定）

# 动态查找 merged 开头的源文件：一个 .txt(CNKI) + 一个 .csv(WOS)
merged_txt = glob.glob(os.path.join(BASE_DIR, 'merged*.txt'))
merged_csv = glob.glob(os.path.join(BASE_DIR, 'merged*.csv'))

if not merged_txt:
    raise FileNotFoundError(f'{BASE_DIR} 下未找到 merged*.txt 文件')
if not merged_csv:
    raise FileNotFoundError(f'{BASE_DIR} 下未找到 merged*.csv 文件')

CNKI_FILE = merged_txt[0]
WOS_FILE  = merged_csv[0]

CK1_OUT = os.path.join(BASE_DIR, 'ck1.txt')
CK2_OUT = os.path.join(BASE_DIR, 'ck2.csv')

print(f'工作目录: {BASE_DIR}')
print(f'目标列表: {CKWX_FILE}')
print(f'CNKI 源 : {os.path.basename(CNKI_FILE)}')
print(f'WOS  源 : {os.path.basename(WOS_FILE)}')


# ===== 1. 读取目标文献名 =====
with open(CKWX_FILE, encoding='utf-8') as f:
    target_titles = [l.strip() for l in f.readlines() if l.strip()]

print(f'\n目标文献数量: {len(target_titles)}')

# 用于追踪匹配状态
matched_titles = set()


# ===== 2. 从 CNKI (.txt) 中提取 → ck1.txt =====
with open(CNKI_FILE, encoding='utf-8') as f:
    cnki_content = f.read()

# 按开头的 [数字] 分割为各条独立记录
records = re.split(r'(?=\[\d+\])', cnki_content)

cnki_matches = []
for rec in records:
    rec_stripped = rec.strip()
    if not rec_stripped:
        continue
    # 去掉 [序号] 前缀，保留正文
    clean_rec = re.sub(r'^\[\d+\]', '', rec_stripped).strip()

    for title in target_titles:
        if title in clean_rec:
            cnki_matches.append(clean_rec)
            matched_titles.add(title)
            print(f'  [CNKI匹配] {title[:40]}')
            break

with open(CK1_OUT, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(cnki_matches))

print(f'\nCNKI: 匹配 {len(cnki_matches)} 条 → ck1.txt')


# ===== 3. 从 WOS (.csv) 中提取 → ck2.csv =====
with open(WOS_FILE, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    wos_rows = list(reader)

print(f'WOS 总记录数: {len(wos_rows)}')

wos_matches = []
for row in wos_rows:
    article_title = row.get('Article Title', '')
    for title in target_titles:
        if (title.lower().strip() == article_title.lower().strip()
                or title in article_title or article_title in title):
            wos_matches.append(row)
            matched_titles.add(title)
            print(f'  [WOS匹配]  {article_title[:50]}')
            break

if wos_matches:
    with open(CK2_OUT, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=wos_matches[0].keys())
        writer.writeheader()
        writer.writerows(wos_matches)

print(f'\nWOS: 匹配 {len(wos_matches)} 条 → ck2.csv')

# ===== 4. 显示未匹配的文献 =====
unmatched = [t for t in target_titles if t not in matched_titles]
if unmatched:
    print(f'\n{"="*50}')
    print(f'未匹配 ({len(unmatched)} 条):')
    for i, t in enumerate(unmatched, 1):
        print(f'  {i}. {t}')
else:
    print('\n全部匹配完成，无遗漏。')

print('\nDone.')

# extract_refs_by_ckwx.py 使用说明

## 功能

根据 `ckwx.txt` 中列出的文献名称，从两个 merged 源文件中自动提取匹配记录，分别输出为 `ck1.txt` 和 `ck2.csv`，输出内容不带序号前缀。

## 文件准备

将以下 **4 个文件** 放在**同一目录**下：

| 文件 | 说明 | 必需 |
|------|------|------|
| `extract_refs_by_ckwx.py` | 本脚本 | 是 |
| `ckwx.txt` | 目标文献名列表，每行一个 | 是 |
| `merged*.txt` | CNKI 合并数据（如 `merged-cnki-20260524-094107.txt`） | 是 |
| `merged*.csv` | WOS 合并数据（如 `merged-wos-20260524-094024.csv`） | 是 |

> 脚本通过 `glob.glob('merged*.txt')` / `merged*.csv` 自动查找，**不需要修改脚本中的文件名**。

## 运行

```bash
cd <文件所在目录>
python extract_refs_by_ckwx.py
```

## 输出

运行后在该目录下生成两个文件：

### ck1.txt（CNKI 中文文献）

- 来源：`merged*.txt`
- 格式：每条记录包含作者、题名、期刊、年份、摘要，条目之间以空行分隔
- 已去除原文件中的 `[1]` `[2]` 等序号前缀

示例：
```
黎世莹,张慧,吕叶辉,姚雪珺,余党会.对AI生成论文摘要的鉴别效能——一项审稿人与AI检测工具的实证研究[J].编辑学报,2026,38(01):82-89.
摘要:分析审稿人、Artificial Intelligence(AI)...

洪涛.AIGC检测的功能反思与规范适用[J].科学学研究,
摘要:为应对AIGC滥用的现实挑战...
```

### ck2.csv（WOS 英文文献）

- 来源：`merged*.csv`
- 格式：标准 CSV，含表头（Authors / Article Title / Source Title / Abstract / Publication Year / DOI）
- UTF-8 BOM 编码（Excel 直接打开不乱码）

## 控制台输出

脚本运行时会打印：

```
工作目录: D:\...\检索内容
目标列表: ...\ckwx.txt
CNKI 源 : merged-cnki-20260524-094107.txt
WOS  源 : merged-wos-20260524-094024.csv

目标文献数量: 30
  [CNKI匹配] 对AI生成论文摘要的鉴别效能——...
  [CNKI匹配] AIGC检测的功能反思与规范适用...
  ...

CNKI: 匹配 16 条 → ck1.txt

WOS 总记录数: 1297
  [WOS匹配] ChatGPT for Education and Research: ...
  ...

WOS: 匹配 6 条 → ck2.csv

==================================================
未匹配 (8 条):
  1. 理解媒介
  2. 中华人民共和国学位法
  ...

Done.
```

## 匹配规则

- **CNKI (.txt)**：以子串方式匹配，检查目标文献名是否出现在记录正文中
- **WOS (.csv)**：对 `Article Title` 字段做精确匹配或双向子串匹配（忽略大小写和首尾空格）

> 未匹配的文献将在末尾集中列出，方便核查是否需要补充数据源。

## 环境要求

- Python 3.6+（仅使用标准库，无需安装第三方包）
- Windows / macOS / Linux 均可运行

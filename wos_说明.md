# wos.py - Web of Science 文献合并去重工具 使用说明

## 📖 工具简介

本工具用于自动合并多个 Web of Science (WOS) 导出的文献数据文件，进行智能去重处理，并输出为标准格式的 CSV 文件，方便后续数据分析和文献管理。

**适用场景：**
- 多次检索 WOS 数据库，产生多个导出文件需要合并
- 需要提取文献的核心字段（标题、作者、期刊、年份、DOI、摘要）
- 需要去除重复文献记录
- 需要将文献数据转换为 CSV 格式以便用 Excel、R、Python 等工具分析

---

## 📥 输入要求

### 文件位置
- 工具会自动处理**当前工作目录**下的文件
- 无需修改代码中的路径配置

### 文件格式
- **格式：** `.xls`（WOS 导出时的默认 Excel 格式）
- **命名规则：** 必须以 `savedrecs` 开头（WOS 导出时的默认文件名前缀）
- **示例：** `savedrecs-1.xls`, `savedrecs-2.xls`, `savedrecs-2026-05-29.xls`

### 字段要求
输入文件应包含以下标准 WOS 导出字段（工具会自动识别并提取）：
- `Article Title` - 文章标题
- `Authors` - 作者
- `Source Title` - 来源期刊/会议名称
- `Publication Year` - 发表年份
- `DOI` - 数字对象标识符
- `Abstract` - 摘要

---

## ⚙️ 处理流程

工具按以下 6 个步骤自动处理：

### 步骤 1：文件扫描
- 自动查找当前目录下所有符合命名规则的 `.xls` 文件
- 显示找到的文件列表
- 如果未找到任何文件，会提示错误并退出

### 步骤 2：字段筛选
- 仅读取并保留 6 个核心字段
- 忽略其他无关字段，减少数据冗余
- 如果某个文件的字段名不匹配，会跳过该文件并提示错误

### 步骤 3：数据合并
- 将所有文件的数据合并到一个数据集中
- 显示合并后的总记录数

### 步骤 4：智能去重
采用两级去重策略：
1. **优先按 DOI 去重**（适用于有 DOI 的正式出版物）
   - 保留第一次出现的记录
   - 删除后续重复的 DOI 记录
2. **DOI 为空的记录按标题去重**（适用于早期文章、会议论文等）
   - 保留第一次出现的记录
   - 删除后续标题相同的记录

### 步骤 5：生成输出文件名
- 自动生成带时间戳的文件名
- 格式：`merged-wos-YYYYMMDD-HHMMSS.csv`
- 示例：`merged-wos-20260529-103827.csv`

### 步骤 6：保存结果
- 输出为 CSV 格式
- 使用 `utf-8-sig` 编码（BOM 编码，Excel 可直接打开且中文无乱码）
- 不使用索引列

---

## 📤 输出说明

### 输出文件
- **文件名：** `merged-wos-YYYYMMDD-HHMMSS.csv`
- **位置：** 当前工作目录
- **编码：** UTF-8 with BOM（Excel 兼容）
- **分隔符：** 逗号（`,`）

### 输出字段
| 字段名 | 说明 | 示例 |
|--------|------|------|
| Article Title | 文章标题 | "Artificial Intelligence in Education: A Review" |
| Authors | 作者列表 | "Smith, J; Zhang, H; Lee, K" |
| Source Title | 期刊/会议名称 | "Computers & Education" |
| Publication Year | 发表年份 | 2025 |
| DOI | 数字对象标识符 | "10.1016/j.compedu.2025.01.001" |
| Abstract | 摘要 | "This paper reviews the applications of AI in education..." |

### 控制台输出示例
```
找到 3 个待处理文件：
  - savedrecs-1.xls
  - savedrecs-2.xls
  - savedrecs-3.xls

✅ 读取成功：savedrecs-1.xls (150 条记录)
✅ 读取成功：savedrecs-2.xls (120 条记录)
✅ 读取成功：savedrecs-3.xls (130 条记录)

合并后总记录数：400 条

===== 去重结果统计 =====
有DOI记录去重：去除 25 条重复记录
无DOI记录去重：去除 15 条重复记录
本次合计去除重复记录：40 条
去重后剩余有效记录数：360 条

🎉 全部处理完成！
📄 最终输出CSV文件：merged-wos-20260529-103827.csv
✅ 最终保留有效记录数：360 条
```

---

## 🚀 使用方法

### 前提条件
已安装 Python 3.6 或更高版本

### 安装依赖
```bash
pip install pandas openpyxl
```
- `pandas`：数据处理核心库
- `openpyxl`：支持读取 `.xls` 和 `.xlsx` 格式

### 操作步骤

1. **将 WOS 导出的文件放入同一目录**
   - 例如：`D:/论文撰写/cnki-wos/`

2. **打开命令行，切换到该目录**
   ```bash
   cd D:/论文撰写/cnki-wos
   ```

3. **运行脚本**
   ```bash
   python wos.py
   ```

4. **查看输出**
   - 控制台会显示处理进度和统计信息
   - 生成的 CSV 文件保存在当前目录

### 用 Excel 打开输出文件
- **方法 1（推荐）：** 直接双击 CSV 文件，Excel 会自动识别 utf-8-sig 编码
- **方法 2：** 如果中文显示乱码，请在 Excel 中：
  1. 点击"数据"选项卡
  2. 选择"获取数据" → "从文本/CSV"
  3. 选择文件，设置文件原始格式为"65001: Unicode (UTF-8)"
  4. 点击"加载"

---

## ⚠️ 注意事项

### 文件命名
- 必须以 `savedrecs` 开头，否则工具无法识别
- WOS 导出时默认使用此外缀，通常无需手动修改

### 字段名匹配
- 工具依赖 WOS 导出的标准字段名
- 如果修改过导出字段设置，可能导致字段无法识别
- 建议使用 WOS 的默认导出字段配置

### 去重规则
- 去重时会保留**第一次出现**的记录（即排在前面的文件中的记录优先）
- 如果同一篇文章在多个文件中出现，仅保留第一次出现的版本
- 去重是基于 DOI 或标题的**精确匹配**，不考虑相似度

### 数据量限制
- 理论上支持无限个输入文件
- 实际受内存限制，通常处理几万条记录无压力
- 如果数据量非常大（>10万条），建议分批处理

### 编码问题
- 输出文件使用 `utf-8-sig` 编码，兼容 Excel
- 如果用其他工具（如 R、Python）读取，建议使用 `utf-8` 编码

---

## 🔧 高级用法

### 修改保留的字段
如果需要保留其他字段，可以修改代码中的 `REQUIRED_FIELDS` 列表：
```python
REQUIRED_FIELDS = [
    "Article Title",
    "Authors",
    "Source Title",
    "Publication Year",
    "DOI",
    "Abstract",
    "Keywords",          # 新增：关键词
    "Cited Reference Count" # 新增：被引次数
]
```

### 修改去重规则
如果需要仅按 DOI 去重（忽略无 DOI 记录的标题去重），可以注释掉相关代码：
```python
# 注释掉以下两行
# no_doi_dedup = no_doi_df.drop_duplicates(subset=[DEDUPLICATE_TITLE_FIELD], keep='first')
# dedup_df = pd.concat([has_doi_dedup, no_doi_dedup], ignore_index=True)
```

### 批量处理不同目录的文件
修改 `INPUT_FOLDER` 变量为绝对路径或相对路径：
```python
INPUT_FOLDER = "D:/论文撰写/WOS数据"
```

---

## ❓ 常见问题

### Q1：工具提示"未找到任何以 savedrecs 开头的 xls 文件"？
**A：**
- 检查文件是否在当前目录
- 检查文件扩展名是否为 `.xls`（不是 `.xlsx` 或 `.txt`）
- 检查文件名是否以 `savedrecs` 开头
- 在命令行中运行 `dir savedrecs*.xls` 确认文件存在

### Q2：某些文件读取失败？
**A：**
- 文件可能损坏，尝试用 Excel 打开确认
- 文件可能被其他程序占用（如 Excel 正在打开），关闭后重试
- 字段名可能不匹配，检查导出时是否使用了自定义字段

### Q3：去重后记录数不对？
**A：**
- 这是正常现象，去重会删除重复记录
- 查看控制台输出的统计信息，了解去重详情
- 如果需要保留所有记录（不去重），可以注释掉去重相关的代码

### Q4：输出的 CSV 文件用 Excel 打开中文乱码？
**A：**
- 工具已使用 `utf-8-sig` 编码，通常无需担心
- 如果仍乱码，请用 Excel 的"数据 → 获取数据 → 从文本/CSV"功能导入
- 或者将文件用记事本打开，另存为 ANSI 编码

### Q5：可以处理 `.xlsx` 格式的文件吗？
**A：**
- 当前版本仅支持 `.xls` 格式
- 可以修改代码中的文件筛选条件：
  ```python
  if f.lower().endswith(('.xls', '.xlsx')) and f.startswith("savedrecs"):
  ```

---

## 📞 技术支持

如有问题或建议，请联系工具开发者。

---

**版本：** 1.0  
**最后更新：** 2026-05-29  
**开发者：** WorkBuddy AI Assistant

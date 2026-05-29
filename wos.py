# 文献数据合并与去重工具 - CSV输出版
# 1. 仅处理：当前目录下 以savedrecs开头 的xls文件
# 2. 字段筛选：仅保留 标题、作者、期刊、年份、DOI、摘要 6个核心字段
# 3. 去重规则：优先按DOI去重，DOI为空的记录按标题去重，重复项仅保留第一条
# 4. 输出文件名：merged-wos-年月日时分秒.csv
import os
from datetime import datetime
import pandas as pd

# ===================== 核心配置项（无需修改）=====================
# 只处理当前目录
INPUT_FOLDER = "."
# 最终保留的核心字段（严格匹配WOS导出的标准字段名）
REQUIRED_FIELDS = [
    "Article Title",    # 标题
    "Authors",          # 作者
    "Source Title",     # 期刊
    "Publication Year", # 年份
    "DOI",              # DOI
    "Abstract"          # 摘要
]
# 去重优先级字段
DEDUPLICATE_DOI_FIELD = "DOI"
DEDUPLICATE_TITLE_FIELD = "Article Title"
# ==========================================================================

def main():
    # 1. 筛选：当前目录下 以savedrecs开头 的 xls 文件
    file_list = []
    for f in os.listdir(INPUT_FOLDER):
        if f.lower().endswith('.xls') and f.startswith("savedrecs"):
            file_list.append(f)

    if not file_list:
        print("错误：当前目录下未找到任何以 savedrecs 开头的 xls 文件")
        return

    print(f"找到 {len(file_list)} 个待处理文件：")
    for f in file_list:
        print(f"  - {f}")

    # 2. 批量读取文件，仅保留目标核心字段
    all_data = []
    for file_name in file_list:
        file_path = os.path.join(INPUT_FOLDER, file_name)
        try:
            df = pd.read_excel(file_path, usecols=REQUIRED_FIELDS)
            all_data.append(df)
            print(f"✅ 读取成功：{file_name} ({len(df)} 条记录)")
        except Exception as e:
            print(f"❌ 读取失败：{file_name}，原因：{str(e)}")
            continue

    if not all_data:
        print("错误：没有成功读取任何有效数据")
        return

    # 3. 合并所有文件数据
    merged_df = pd.concat(all_data, ignore_index=True)
    print(f"\n合并后总记录数：{len(merged_df)} 条")

    # 4. 核心去重逻辑：优先按DOI去重，DOI为空按标题去重
    # 拆分数据：有DOI的记录 + 无DOI的记录
    has_doi_df = merged_df[merged_df[DEDUPLICATE_DOI_FIELD].notna() & (merged_df[DEDUPLICATE_DOI_FIELD] != "")]
    no_doi_df = merged_df[merged_df[DEDUPLICATE_DOI_FIELD].isna() | (merged_df[DEDUPLICATE_DOI_FIELD] == "")]

    # 有DOI的记录：按DOI去重，保留第一条
    has_doi_dedup = has_doi_df.drop_duplicates(subset=[DEDUPLICATE_DOI_FIELD], keep='first')
    # 无DOI的记录：按标题去重，保留第一条
    no_doi_dedup = no_doi_df.drop_duplicates(subset=[DEDUPLICATE_TITLE_FIELD], keep='first')

    # 合并去重后的两部分数据
    dedup_df = pd.concat([has_doi_dedup, no_doi_dedup], ignore_index=True)

    # 去重统计
    total_removed = len(merged_df) - len(dedup_df)
    doi_removed = len(has_doi_df) - len(has_doi_dedup)
    title_removed = len(no_doi_df) - len(no_doi_dedup)

    print(f"\n===== 去重结果统计 =====")
    print(f"有DOI记录去重：去除 {doi_removed} 条重复记录")
    print(f"无DOI记录去重：去除 {title_removed} 条重复记录")
    print(f"本次合计去除重复记录：{total_removed} 条")
    print(f"去重后剩余有效记录数：{len(dedup_df)} 条")

    # 5. 生成带当前日期时间的CSV输出文件名
    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    OUTPUT_FILE = f"merged-wos-{current_time}.csv"

    # 6. 保存为标准CSV文件，utf-8-sig编码避免中文乱码
    dedup_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig', sep=',')

    print(f"\n🎉 全部处理完成！")
    print(f"📄 最终输出CSV文件：{OUTPUT_FILE}")
    print(f"✅ 最终保留有效记录数：{len(dedup_df)} 条")

if __name__ == "__main__":
    main()
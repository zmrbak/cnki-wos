import re
import os
from datetime import datetime
from collections import OrderedDict

def merge_and_deduplicate_literature(output_dir: str = "."):
    """
    自动合并当前目录下所有 CNKI 开头的 txt 文件
    去重 + 重新排序号 + 按时间生成输出文件
    """
    # 1. 获取当前目录下所有 CNKI 开头的 .txt 文件
    file_list = [
        f for f in os.listdir(".")
        if f.startswith("CNKI") and f.endswith(".txt") and os.path.isfile(f)
    ]

    if not file_list:
        print("❌ 当前目录下未找到任何 CNKI 开头的 txt 文件")
        return

    print(f"✅ 找到 {len(file_list)} 个文献文件：")
    for f in file_list:
        print(f"   - {f}")

    # 2. 去重存储（有序 + 不重复）
    literature_dict = OrderedDict()
    pattern = re.compile(r'\[(\d+)\](.*?)(?=\n\[|\n*$)', re.DOTALL)

    # 3. 读取所有文件
    for file_name in file_list:
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️ 读取失败 {file_name}：{str(e)}")
            continue

        # 提取 [1]xxx [2]xxx 格式条目
        matches = pattern.findall(content)
        for _, text in matches:
            clean_text = re.sub(r'\s+', ' ', text).strip()
            if clean_text:
                literature_dict[clean_text] = text.strip()

    # 4. 生成输出文件名：merged-cnki-年月日时分秒.txt
    time_str = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = os.path.join(output_dir, f"merged-cnki-{time_str}.txt")

    # 5. 写入结果（重新编号）
    with open(output_file, 'w', encoding='utf-8') as f:
        for idx, content in enumerate(literature_dict.values(), 1):
            f.write(f"[{idx}]{content}\n")

    print("\n🎉 合并去重完成！")
    print(f"📊 去重后总文献数：{len(literature_dict)}")
    print(f"📁 输出文件：{output_file}")

if __name__ == '__main__':
    merge_and_deduplicate_literature()
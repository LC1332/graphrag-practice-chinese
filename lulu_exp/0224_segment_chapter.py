'''
在local_data/raw_input.txt中，存着以 GB2312 编码的原文

我希望抽取这中间所有的章节行 章节行的特点是会以

第xx章 开头，其中xx是汉字的数字，可能包括一到九，零，十，百，千 这几个汉字

所以我们可以用正则表达式来提取这些行

先帮我实现一个python程序，统计出原文所有的章节行
'''

'''
这段代码可以顺利运行，我希望将
'''
import re
import os

# 定义正则表达式，匹配章节行
chapter_pattern = re.compile(r'^第([零一二三四五六七八九十百千]+)章')

# 读取文件并提取章节内容
def extract_and_save_chapters(file_path, output_dir):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    current_chapter = None
    current_content = []

    count = 0

    for line in content:
        match = chapter_pattern.match(line)
        if match:
            # 如果已经有一个章节在处理，保存当前章节内容到文件
            if current_chapter:

                save_chapter(current_chapter, current_content, output_dir, count)
                count += 1
                current_content = []  # 重置当前章节内容

            current_chapter = line.strip()  # 更新当前章节名

            if count > 700:
                return
        else:
            if current_chapter:
                current_content.append(line)

    # 保存最后一个章节的内容
    if current_chapter:
        save_chapter(current_chapter, current_content, output_dir)

# 保存章节内容到文件
def save_chapter(chapter_name, content, output_dir, save_index):
    # 创建输出目录（如果不存在）
    os.makedirs(output_dir, exist_ok=True)

    # 以4位save_index + chapter_name作为文件名
    file_name = f"{save_index:04d}_book.txt"
    # file_name = f"{chapter_name}.txt"


    file_path = os.path.join(output_dir, file_name)

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        # 把章节名写入文件
        file.writelines(chapter_name + '\n\n')
        file.writelines(content)

    print(f"已保存章节: {chapter_name} 到 {file_path}")

# 文件路径
file_path = 'local_data/raw_input.txt'
output_dir = 'local_data/input'

# 提取并保存章节内容
extract_and_save_chapters(file_path, output_dir)
import os
import re

# 定义目标目录和目标文件类型
directory_path = r'C:\Users\wdlam\Desktop\02项目代码\test\test2'  # 使用原始字符串，避免转义
file_extensions = ['.kjb', '.ktr']

# 遍历目录及其子目录并查找指定类型的文件
target_files = []
for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file.lower().endswith(tuple(file_extensions)):
            target_files.append(os.path.join(root, file))

# 写入文件的路径
output_file_path = 'matched_tables.txt'
# 清空文件内容
open(output_file_path, 'w').close()

# 定义正则表达式模式，匹配表名，前后不包含英文逗号、"and"、"when" (忽略大小写) 或 "= "（前有空格）
# pattern = r"\b(?<![Ss][Ee][Ll][Ee][Cc][Tt])(?<![Ww][Hh][Ee][Nn])(?<![Ww][Hh][Ee][Rr][Ee])(?<![Tt][Hh][Ee][Nn])(?<![Ee][Ll][Ss][Ee])(?<![Aa][Nn][Dd])(?<![Bb][Yy])(?<![,])(?<![-])\s((?:[A-Za-z0-9_]+\.){1,2}[A-Za-z0-9_\u4e00-\u9fa5]+)\b(?!\s*=)(?!=)(?!\s*[,])(?!\s[Aa][Nn][Dd])(?!\s[Ee][Nn][Dd])(?!\s[Ff][Rr][Oo][Mm])"
pattern = r"\b(?:FROM|TABLE|INTO|EXISTS|JOIN|UPDATE)\s+(?<![Ss][Ee][Ll][Ee][Cc][Tt])(?<![Ww][Hh][Ee][Nn])(?<![Ww][Hh][Ee][Rr][Ee])(?<![Tt][Hh][Ee][Nn])(?<![Ee][Ll][Ss][Ee])(?<![Aa][Nn][Dd])(?<![Bb][Yy])(?<![,])(?<![-])((?:[A-Za-z0-9_]+\.){1,2}[A-Za-z0-9_\u4e00-\u9fa5]+)\b(?!\s*=)(?!=)(?!\s*[,])(?!\s[Aa][Nn][Dd])(?!\s[Ee][Nn][Dd])(?!\s[Ff][Rr][Oo][Mm])"
# 用于存储所有匹配结果的集合，以确保唯一性
all_matches = set()

# 读取文件内容并提取匹配的表名
for file_path in target_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f'内容读取成功: {file_path}')
            open(output_file_path, 'a').write(file_path + '\n')

            # 使用正则表达式查找所有匹配项，并添加到集合中
            matches = set(re.findall(pattern, content))
            all_matches.update(matches)

            # print(matches)
            # print(f"匹配条数: {len(matches)}")

            with open(output_file_path, 'a') as file:
                for match in all_matches:
                    file.write(match + '\n')
                    print(f"匹配到的表名: {match}")
            # print(f"匹配到的表名: {match}", end='')

    except Exception as e:
        print(f'读取文件时出错: {file_path}')
        print(e)

# 最终将所有唯一的匹配项写入输出文件
# with open(output_file_path, 'a') as file:
#     for match in all_matches:
#         file.write(match + '\n')
        # print(f"匹配到的表名: {match}", end='')

print(f"总共匹配到的唯一表名数量: {len(all_matches)}")

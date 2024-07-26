import re

# 测试字符串
test_string = "CASE WHEN T.YSP1D = '合格' THEN T.SL ELSE T.S12L - T.SL_1YWC END SL_QUALIFIED,"

# 定义正则表达式模式，排除前面有 "WHEN "、逗号、"AND " 的情况，匹配表名或字段名
pattern = r"(?<![Ww][Hh][Ee][Nn])(?<![Tt][Hh][Ee][Nn])(?<![Ee][Ll][Ss][Ee])(?<![,])(?<![-])(?<![Aa][Nn][Dd])\s([A-Za-z0-9_]+\.[A-Za-z0-9_]+)(?=[\s,]|$)(?<!\s[Aa][Nn][Dd])(?<!\s[Ee][Nn][Dd])(?<!\s=)"

# 使用正则表达式查找所有匹配项，并去重
matches = set(re.findall(pattern, test_string))

# 打印去重后的表名或字段名
for match in matches:
    print(f"匹配到的表名或字段名: {match}")

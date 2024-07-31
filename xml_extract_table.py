import os
import re
from lxml import etree as ET
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML

# 通过sqlparse从SQL中提取表名
def extract_tables(sql):
    tables = set()
    parsed = sqlparse.parse(sql)
    for statement in parsed:
        from_seen = False
        for token in statement.tokens:
            # 查找INSERT INTO、CREATE TABLE之后的表名
            if token.ttype is Keyword and token.value.upper() in ('INTO', 'TABLE', 'TRUNCATE'):
                next_token = statement.token_next(statement.token_index(token))
                if isinstance(next_token, Identifier):
                    tables.add(next_token.get_real_name())
                elif isinstance(next_token, IdentifierList):
                    for identifier in next_token.get_identifiers():
                        tables.add(identifier.get_real_name())

            # 查找FROM和JOIN之后的表名
            if token.ttype is Keyword and token.value.upper() in ('FROM', 'JOIN'):
                from_seen = True
            if from_seen and isinstance(token, IdentifierList):
                for identifier in token.get_identifiers():
                    tables.add(identifier.get_real_name())
                from_seen = False
            elif from_seen and isinstance(token, Identifier):
                tables.add(token.get_real_name())
                from_seen = False

    return tables

# 通过正则表达式提取表名
def extract_tables_re(sql):
    # 定义正则表达式模式，匹配表名，前后不包含英文逗号、"and"、"when" (忽略大小写) 或 "= "（前有空格）
    pattern = r"\b(?:FROM|TABLE|INTO|EXISTS|JOIN|UPDATE)\s+(?<![Ss][Ee][Ll][Ee][Cc][Tt])(?<![Ww][Hh][Ee][Nn])(?<![Ww][Hh][Ee][Rr][Ee])(?<![Tt][Hh][Ee][Nn])(?<![Ee][Ll][Ss][Ee])(?<![Aa][Nn][Dd])(?<![Bb][Yy])(?<![,])(?<![-])((?:[A-Za-z0-9_]+\.){1,2}[A-Za-z0-9_\u4e00-\u9fa5]+)\b(?!\s*=)(?!=)(?!\s*[,])(?!\s[Aa][Nn][Dd])(?!\s[Ee][Nn][Dd])(?!\s[Ff][Rr][Oo][Mm])"
    # 使用正则表达式查找所有匹配项，并添加到集合中
    matches = set(re.findall(pattern, sql, re.IGNORECASE))

    return matches


# 定义目标目录和目标文件类型
directory_path = r'C:\Users\wdlam\Desktop\02项目代码\test\test2'  # 使用原始字符串，避免转义
file_extensions = ['.kjb', '.ktr']

# 遍历目录及其子目录并查找指定类型的文件
target_files = []
for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file.lower().endswith(tuple(file_extensions)):
            target_files.append(os.path.join(root, file))

# 读取文件内容并提取匹配的表名
for file_path in target_files:
    # 解析XML文件
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 查找所有名为sql的节点
    sql_nodes = root.findall('.//sql')

    # 对于每个sql节点，查找同级的name节点
    for sql in sql_nodes:
        parent = sql.getparent()  # 使用lxml的getparent()方法获取父节点
        if parent is not None:
            name = parent.find('name')
            type_ = parent.find('type')
            connection = parent.find('connection')
            copies = parent.find('copies')
            schema = parent.find('schema')

            sql_text = sql.text.strip() if sql.text else "None"
            name_text = name.text.strip() if name is not None and name.text else "None"
            type_text = type_.text.strip() if type_ is not None and type_.text else "None"
            connection_text = connection.text.strip() if connection is not None and connection.text else "None"
            copies_text = copies.text.strip() if copies is not None and copies.text else "None"
            schema_text = schema.text.strip() if schema is not None and schema.text else "None"

            file_name = os.path.basename(file_path)
            print(f"FileName: {file_name}")
            print(f"FilePath: {file_path}")
            print(f"Name: {os.path.splitext(file_name)[0]}")
            print(f"Type: {type_text}")
            print(f"Connection: {connection_text}")
            print(f"Schema: {schema_text}")
            print(f"ModType: {name_text}")

            # 定义正则表达式模式，匹配表名，前后不包含英文逗号、"and"、"when" (忽略大小写) 或 "= "（前有空格）
            # pattern = r"\b(?<![Ss][Ee][Ll][Ee][Cc][Tt])(?<![Ww][Hh][Ee][Nn])(?<![Ww][Hh][Ee][Rr][Ee])(?<![Tt][Hh][Ee][Nn])(?<![Ee][Ll][Ss][Ee])(?<![Aa][Nn][Dd])(?<![Bb][Yy])(?<![,])(?<![-])\s((?:[A-Za-z0-9_]+\.){1,2}[A-Za-z0-9_\u4e00-\u9fa5]+)\b(?!\s*=)(?!=)(?!\s*[,])(?!\s[Aa][Nn][Dd])(?!\s[Ee][Nn][Dd])(?!\s[Ff][Rr][Oo][Mm])"
            pattern = r"\b(?:FROM|TABLE|INTO|EXISTS|JOIN|UPDATE)\s+(?<![Ss][Ee][Ll][Ee][Cc][Tt])(?<![Ww][Hh][Ee][Nn])(?<![Ww][Hh][Ee][Rr][Ee])(?<![Tt][Hh][Ee][Nn])(?<![Ee][Ll][Ss][Ee])(?<![Aa][Nn][Dd])(?<![Bb][Yy])(?<![,])(?<![-])((?:[A-Za-z0-9_]+\.){1,2}[A-Za-z0-9_\u4e00-\u9fa5]+)\b(?!\s*=)(?!=)(?!\s*[,])(?!\s[Aa][Nn][Dd])(?!\s[Ee][Nn][Dd])(?!\s[Ff][Rr][Oo][Mm])"
            # 用于存储所有匹配结果的集合，以确保唯一性
            all_matches = set()

            # 提取表名
            tables = extract_tables_re(sql_text)
            print(f"Tables: {tables}")

            # sql = """
            #     insert into GKHT_BYJ.dbo.DW_Data_related_Tab (
            #         FileName,
            #         FilePath,
            #         Name,
            #         Type,
            #         Conncetion,
            #         Schema,
            #         ModType,
            #         Table,
            #         InsDD
            #     ) values (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            # """
            # cursor.execute(
            #     sql,
            #     (
            #         f"{file_name}",
            #         file_path,
            #         os.path.splitext(file_name)[0],
            #         type_text,
            #         connection_text,
            #         schema_text,
            #         name_text,
            #         table_name
            #     )
            # )
            # print(sSql01)
            # print(f"SQL: {sql_text}")
            print("-" * 40)
        else:
            print(f"SQL: {sql.text} (No corresponding parent node found)")


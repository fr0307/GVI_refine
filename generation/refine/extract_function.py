import re
import os

from config import gen_final_output_root, gen_extracted_output_root


def extract_all_refined():
    count = 0

    if not os.path.exists(gen_extracted_output_root):
        os.mkdir(gen_extracted_output_root)

    dirs = os.listdir(gen_final_output_root)
    for dir_name in dirs:
        input_dir_path = os.path.join(gen_final_output_root, dir_name)
        output_dir_path = os.path.join(gen_extracted_output_root, dir_name)

        if not os.path.exists(output_dir_path):
            os.mkdir(output_dir_path)

        files = os.listdir(input_dir_path)
        for file in files:
            input_file_path = os.path.join(input_dir_path, file)
            output_file_path = os.path.join(output_dir_path, file)
            with open(input_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            try:
                extracted_function = extract_largest_function(content)
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(extracted_function)
                count += 1
            except ValueError as ve:
                print(f"Value Error occurred, dir {dir_name}, file {file}")
                print(ve)
                print(content)
            except Exception as e:
                print(f"Unexpected error, dir {dir_name}, file {file}")
                print(e)

    print(f"{count} files extracted successfully")


def remove_comments(code):
    """去除 C/C++ 代码中的注释，同时保留字符串字面量"""
    result = []
    i = 0
    in_single_quote = False  # 处理字符字面量 'c'
    in_double_quote = False  # 处理字符串 "abc"
    in_comment = False

    while i < len(code):
        if in_comment:
            # 结束多行注释 */
            if code[i:i+2] == '*/':
                in_comment = False
                i += 2
            else:
                i += 1
        elif in_single_quote:
            # 处理字符字面量结束 '
            if code[i] == "'" and code[i-1] != "\\":
                in_single_quote = False
            result.append(code[i])
            i += 1
        elif in_double_quote:
            # 处理字符串结束 "
            if code[i] == '"' and code[i-1] != "\\":
                in_double_quote = False
            result.append(code[i])
            i += 1
        else:
            # 处理单行注释 //
            if code[i:i+2] == "//":
                i = code.find("\n", i)  # 直接跳到行末
                if i == -1:
                    break
            # 处理多行注释 /*
            elif code[i:i+2] == "/*":
                in_comment = True
                i += 2
            # 处理字符串字面量 "
            elif code[i] == '"':
                in_double_quote = True
                result.append(code[i])
                i += 1
            # 处理字符字面量 '
            elif code[i] == "'":
                in_single_quote = True
                result.append(code[i])
                i += 1
            else:
                result.append(code[i])
                i += 1

    return "".join(result)


def extract_largest_function(c_code: str) -> str:
    # 去除预处理指令
    c_code = re.sub(r'^[ \t]*#.*', '', c_code, flags=re.MULTILINE)

    # 过滤掉 typedef struct 及普通 struct 定义
    c_code = re.sub(r'typedef\s+struct\s+\w*\s*\{[^}]*\}\s+\w+\s*;?', '', c_code, flags=re.MULTILINE | re.DOTALL)
    c_code = re.sub(r'struct\s+\w+\s*\{[^}]*\}\s*;?', '', c_code, flags=re.MULTILINE | re.DOTALL)

    # 去除单行注释
    c_code = remove_comments(c_code)

    # 匹配函数定义（支持指针返回值）
    func_pattern = re.finditer(
        # r'(?:public|private|protected)?\s*'  # 匹配访问修饰符
        # r'(?:static|inline|virtual)?\s*'  # 匹配修饰符
        r'[a-zA-Z_][a-zA-Z0-9_\s\*]*\*?\s*'  # 匹配返回类型
        r'[a-zA-Z_][a-zA-Z0-9_]*\s*'  # 匹配函数名
        r'\([^)]*\)\s*\{',  # 匹配参数列表和 {
        c_code, re.MULTILINE
    )

    functions = []

    for match in func_pattern:
        start_idx = match.start()
        func_header = match.group()
        func_name_match = re.search(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', func_header)
        if not func_name_match:
            continue
        func_name = func_name_match.group(1)

        # 手动匹配大括号内容
        brace_count = 0
        end_idx = start_idx
        for i in range(start_idx, len(c_code)):
            if c_code[i] == '{':
                brace_count += 1
            elif c_code[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break

        func_code = c_code[start_idx:end_idx]
        line_count = func_code.count('\n')
        functions.append((func_name, line_count, func_code))

    if not functions:
        raise ValueError("No functions found in the provided C code.")

    # 按行数排序
    functions.sort(key=lambda x: x[1], reverse=True)

    # 跳过 main，选择行数最多的非 main 函数
    for func_name, _, func_code in functions:
        if func_name != 'main':
            return func_code

    # 如果 main 是唯一函数，则报错
    raise ValueError("Only 'main' function found, no other function available.")


if __name__ == '__main__':
    extract_all_refined()




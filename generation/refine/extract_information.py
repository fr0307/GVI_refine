import json
import os
import re
from tqdm import tqdm

from config import cur_gen_output_root, pattern_output, type_output, gen_discarded_output_root
from generation.config import gen_combine_output, rm_comments_output
from GVI_regen_context import re_gen_context, extract_code


pattern_reg = r"Base on step 2, extract the vulnerability pattern\. Please limit your response to no more than 100 tokens\.\s*AI:(.*?)\s*Human: "
type_reg = r"Base on step 1, identify the type of security vulnerability present in the example function code\. Please limit your response to no more than 100 tokens\.\s*AI:(.*?)\s*Human: "


def check_output_dir(path):
    root = os.path.dirname(path)
    if not os.path.exists(root):
        os.mkdir(root)


def extract(text, reg):
    match = re.search(reg, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return ''


def extract_pattern(text):
    return extract(text, pattern_reg)


def extract_vul_type(text):
    return extract(text, type_reg)


def remove_comments(code):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        if match.group(2) is not None:
            return ""  # so comments will be replaced by nothing
        else:  # returns the literal strings
            return match.group(1)

    return regex.sub(_replacer, code)


def remove_selected_structs(code):
    # Remove all #include statements
    code = re.sub(r'#include[^\n]*', '', code)
    code = re.sub(r'#define[^\n]*', '', code)

    # Remove typedef struct with {}
    code = re.sub(r'typedef\s+struct\s+\w*\s*\{[^}]*\}\s*\w+;', '', code, flags=re.DOTALL)
    code = re.sub(r'typedef\s+struct\s*\{[^}]*\}\s*\w+;', '', code, flags=re.DOTALL)
    code = re.sub(r'typedef\s+struct\s+\w*\s*\{[^}]*\}\s*\w+,\s*\*?\w+;', '', code, flags=re.DOTALL)

    code = re.sub(r'typedef\s+enum\s*\{([^\}]*)\}\s*(\w+);', '', code, flags=re.DOTALL)
    return code


def rm_comments():
    with open('../' + gen_combine_output, 'r') as f:
        data = json.load(f)
    for item in data:
        item['code'] = remove_comments(item['code'])
        item['code'] = remove_selected_structs(item['code'])
    with open('../' + rm_comments_output, 'w') as f:
        json.dump(data, f, indent=4)


def extract_all():
    if not os.path.exists(gen_discarded_output_root):
        os.mkdir(gen_discarded_output_root)

    dirs = os.listdir(cur_gen_output_root)
    code_gen = []
    pattern_gen, type_gen = {}, {}
    code_count, pattern_count, type_count = 0, 0, 0
    for i in tqdm(range(len(dirs)), desc="Processing", unit="item"):
        dir = os.path.join(cur_gen_output_root, str(i))
        files = os.listdir(dir)
        for file in files:
            if not file.endswith('.c'):  # Skip files that are not .c files
                continue
            file_path = os.path.join(dir, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    context = f.read()
                except UnicodeDecodeError as e:
                    print(f'{file_path}:\tUnicodeDecodeError, {e}')
                    continue

            code_matches = extract_code(context)
            if not len(code_matches) == 4:
                # save the old context as 'extracted'
                discarded_file_path = os.path.join(gen_discarded_output_root, str(i), file)
                check_output_dir(discarded_file_path)
                with open(discarded_file_path, 'w', encoding='utf-8') as f:
                    f.write(context)

                # regen a context that fit the format
                context = re_gen_context(i)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(context)
                code_matches = extract_code(context)

            for num, match in enumerate(code_matches):
                file = str(i) + '_' + str(num) + '_1.c'
                ex = {
                    'id': code_count,
                    'file_name': file,
                    'file_path': file_path.split("../", 1)[1],
                    'code': match,
                    'label': 1
                }
                code_count += 1
                code_gen.append(ex)

            pattern = extract_pattern(context)
            pattern_gen[file_path.split("../", 1)[1]] = pattern
            if pattern != '':
                pattern_count += 1
            else:
                print(f'pattern extract error : pos {i}')

            vul_type = extract_vul_type(context)
            type_gen[file_path.split("../", 1)[1]] = vul_type
            if vul_type != '':
                type_count += 1
            else:
                print(f'type extract error : pos {i}')

    check_output_dir('../' + gen_combine_output)
    with open('../' + gen_combine_output, 'w') as f:
        json.dump(code_gen, f, indent=4)
        print(f'gen: {len(code_gen)}')

    rm_comments()

    check_output_dir(pattern_output)
    with open(pattern_output, 'w') as f:
        json.dump(pattern_gen, f, indent=4)
        print(f'{pattern_count} patterns extracted successfully')

    check_output_dir(type_output)
    with open(type_output, 'w') as f:
        json.dump(type_gen, f, indent=4)
        print(f'{type_count} types extracted successfully')


if __name__ == "__main__":
    extract_all()

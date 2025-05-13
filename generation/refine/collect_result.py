import os
import json
from tqdm import tqdm

from config import gen_final_output_root, collected_original_raw_code_root, collected_refined_raw_code_root
from generation.config import rm_comments_output
cur_rm_comments_output = '../' + rm_comments_output


def collect_original_code():
    with open(cur_rm_comments_output, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if not os.path.exists(collected_original_raw_code_root):
        os.mkdir(collected_original_raw_code_root)
    for index, item in enumerate(tqdm(data)):
        output_path = collected_original_raw_code_root + f'/{index}.c'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(item['code'])


def collect_refined_code():
    if not os.path.exists(collected_refined_raw_code_root):
        os.mkdir(collected_refined_raw_code_root)
    dirs = os.listdir(gen_final_output_root)
    for dir in tqdm(dirs):
        dir_path = os.path.join(gen_final_output_root, dir)
        files = os.listdir(dir_path)
        for file in files:
            load_file_path = os.path.join(dir_path, file)
            save_file_path = os.path.join(collected_refined_raw_code_root, file)
            with open(load_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(save_file_path, 'w', encoding='utf-8') as f:
                f.write(content)


if __name__ == "__main__":
    collect_original_code()
    collect_refined_code()

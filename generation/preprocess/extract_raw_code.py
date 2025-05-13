import json
import pandas as pd
import os
from tqdm import tqdm
from generation.config import origin_data
from generation.refine.config import collected_refined_raw_code_root, collected_original_raw_code_root


def extract_devign_raw_code():
    save_code_dir = "./raw_code/devign/"

    if not os.path.exists(save_code_dir):
        os.mkdir(save_code_dir)

    with open('../' + origin_data, 'r', encoding='utf-8') as file:
        data = json.load(file)

        for index, item in enumerate(tqdm(data)):
            save_code_file_path = os.path.join(save_code_dir, f'ori_{index}_{item["target"]}.c')

            with open(save_code_file_path, 'w', encoding='utf-8') as f:
                f.write(item['func'])

def extract_reveal_raw_code():
    save_code_dir = "./raw_code/reveal/"

    if not os.path.exists(save_code_dir):
        os.mkdir(save_code_dir)

    with open('../origin_data_reveal/non-vulnerables.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        for index, item in enumerate(tqdm(data)):
            save_code_file_path = os.path.join(save_code_dir, f'ori_{index}_0.c')

            with open(save_code_file_path, 'w', encoding='utf-8') as f:
                f.write(item['code'])

    with open('../origin_data_reveal/vulnerables.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        for index, item in enumerate(tqdm(data)):
            save_code_file_path = os.path.join(save_code_dir, f'ori_{index}_1.c')

            with open(save_code_file_path, 'w', encoding='utf-8') as f:
                f.write(item['code'])




def extract_bigvul_raw_code():
    csv_path = "../../../../Data Refine Test/database/MSR_data_cleaned/MSR_data_cleaned.csv"
    output_dir = "./raw_code/bigvul/"
    chunksize = 1000

    os.makedirs(output_dir, exist_ok=True)

    total_index = 0

    for chunk in pd.read_csv(csv_path, chunksize=chunksize):
        for i, row in chunk.iterrows():
            func_before = row.get('func_before', '')
            vul = row.get('vul')

            if total_index == 178498 or total_index == 183122:  # 检查是否为目标索引
                df = pd.read_csv(csv_path, nrows=0)
                print(f"Row at index {i}:")
                for column in df.columns:
                    print(f"{column:30} : {row[column]}")

            if pd.isna(func_before):  # 跳过空函数
                total_index += 1
                continue

            # filename = f"{total_index}_{int(vul)}.c"
            # filepath = os.path.join(output_dir, filename)
            #
            # with open(filepath, 'w', encoding='utf-8') as f:
            #     f.write(func_before)

            total_index += 1


def extract_generated_raw_code(code_num=None):
    save_code_dir = "./raw_code/devign/"
    refined_code_dir = os.path.join("../refine/", collected_refined_raw_code_root)

    if not os.path.exists(save_code_dir):
        os.mkdir(save_code_dir)

    file_names = os.listdir(refined_code_dir)

    file_names.sort(key=lambda x: int(x.split('.')[0]))

    code_count = 0
    for file_name in tqdm(file_names):
        ori_file_path = os.path.join(refined_code_dir, file_name)
        with open(ori_file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        index = int(file_name.split('.')[0])
        save_file_path = os.path.join(save_code_dir, f'ref_{index}_1.c')
        with open(save_file_path, 'w', encoding='utf-8') as f:
            f.write(code)

        code_count += 1
        if code_num is not None and code_count >= code_num:
            break


def extract_gvi_raw_code(code_num=None):
    save_code_dir = "./raw_code/devign/"
    refined_code_dir = os.path.join("../refine/", collected_original_raw_code_root)

    if not os.path.exists(save_code_dir):
        os.mkdir(save_code_dir)

    file_names = os.listdir(refined_code_dir)

    file_names.sort(key=lambda x: int(x.split('.')[0]))

    code_count = 0
    for file_name in tqdm(file_names):
        ori_file_path = os.path.join(refined_code_dir, file_name)
        with open(ori_file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        index = int(file_name.split('.')[0])
        save_file_path = os.path.join(save_code_dir, f'gvi_{index}_1.c')
        with open(save_file_path, 'w', encoding='utf-8') as f:
            f.write(code)

        code_count += 1
        if code_num is not None and code_count >= code_num:
            break


if __name__ == '__main__':
    extract_devign_raw_code()
    # extract_generated_raw_code()
    extract_gvi_raw_code(code_num=2398)
    # extract_reveal_raw_code()
    # extract_bigvul_raw_code()
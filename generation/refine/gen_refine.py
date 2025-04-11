from tqdm import tqdm
import json
import os
import re

from generation.config import OPENAI_API_KEY, gen_combine_output, rm_comments_output
from config import pattern_output, type_output, MAX_ITER_NUM, gen_final_output_root
from iter_judge import judge_vulnerable
from iter_feedback import feedback
from iter_refine import refine
from iter_inject import inject
from GVI_re_gen import re_gen

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def get_output_path(dir, index, file_name):
    if not os.path.exists(dir):
        os.mkdir(dir)
    output_dir = os.path.join(dir, str(index))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_path = os.path.join(output_dir, file_name)
    return output_path


def self_refine(start_index=None, end_index=None):
    # with open(pattern_output, 'r') as f:
    #     patterns = json.load(f)

    with open(type_output, 'r') as f:
        vul_types = json.load(f)

    # with open('../'+rm_comments_output, 'r') as f:
    #     origin_data = json.load(f)

    with open('../'+gen_combine_output, 'r') as f:
        origin_data = json.load(f)

    for index, item in enumerate(tqdm(origin_data)):
        # auto stop
        if (start_index is not None) and (index < start_index):
            continue
        if (end_index is not None) and (index >= end_index):
            return

        code = item['code']
        vul_type = vul_types[item['file_path']]

        while not judge_vulnerable(code):
            origin_index = int(item['file_name'].split('_')[0])
            regen_res = re_gen(origin_index)
            code = regen_res['code']
            vul_type = regen_res['vul_type']

        for iteration in range(MAX_ITER_NUM):

            feedback_content, step, early_stop_flag = feedback(code, index, iteration)

            if early_stop_flag:
                break

            refined_code = refine(code, feedback_content, index, iteration, step)

            if judge_vulnerable(refined_code):
                code = refined_code

                final_file_path = get_output_path(gen_final_output_root, index, f"{index}.c")
                with open(final_file_path, 'w', encoding="utf-8") as f:
                    f.write(code)


if __name__ == "__main__":
    self_refine(end_index=41)

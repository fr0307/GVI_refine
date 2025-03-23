from tqdm import tqdm
import json
import os
import re

from generation.config import OPENAI_API_KEY, gen_combine_output, rm_comments_output
from config import pattern_output, type_output, MAX_ITER_NUM, refine_end_reg, judge_reg, gen_final_output_root
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

        # judge_key = False  # 为True时代表已经refine一次，不再进行重新生成，而是再次判断是否有对应漏洞
        early_stop_key = False  # 判断当前代码是否被判定为可以early-stop，如果是，通过一次漏洞检测后就可以停止
        for iteration in range(MAX_ITER_NUM+1):
            vul_judge, memory, step = judge_vulnerable(code, vul_type, index, iteration)

            # if doesn't contain vulnerability, recall GVI / inject
            if not vul_judge:

                # # code had passed judge before, try again
                # if judge_key:
                #     continue

                # early stopping were enabled, but the code didn't pass vul check, refuse early stopping
                if early_stop_key:
                    early_stop_key = False

                if iteration == MAX_ITER_NUM:
                    break

                # regen none_vulnerable data
                origin_index = int(item['file_name'].split('_')[0])
                regen_res = re_gen(origin_index)
                code = regen_res['code']
                vul_type = regen_res['vul_type']

                # inject vulnerability into none_vulnerable data
                # inject_res = inject(code, vul_type, index, iteration, memory, step)
                # code = inject_res['code']

            else:
                # judge_key = True

                final_file_path = get_output_path(gen_final_output_root, index, f"{index}.c")
                with open(final_file_path, 'w', encoding="utf-8") as f:
                    f.write(code)

                # has reach max iter number or stop early is enabled, stop after a final vul judge
                if iteration == MAX_ITER_NUM or early_stop_key:
                    break

                feedback_content, memory, step = feedback(index, iteration, memory, step)

                # early stopping
                if re.search(refine_end_reg, feedback_content):
                    early_stop_key = True
                    continue

                code = refine(code, index, iteration, memory, step)
                memory.clear()


if __name__ == "__main__":
    self_refine(end_index=41)

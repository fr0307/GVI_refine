import random

from extract_information import extract_pattern, extract_vul_type
from GVI_regen_context import re_gen_context, extract_code


def re_gen(origin_index):
    context = re_gen_context(origin_index)

    res = {}
    pattern = extract_pattern(context)
    vul_type = extract_vul_type(context)

    res['pattern'] = pattern
    res['vul_type'] = vul_type

    # matches = extract_code(context, 'text')
    # if len(matches) == 5 or \
    #         len(matches) == 6 or \
    #         len(matches) == 7 or \
    #         len(matches) == 8 or \
    #         len(matches) == 9 or \
    #         len(matches) == 10 or \
    #         len(matches) == 19:
    #     index = random.randint(1, len(matches) - 1)
    #     # select a random example as the re-gen output
    #     res['code'] = matches[index]
    #     return res
    # elif len(matches) == 1 or len(matches) == 2:
    #     match = matches[-1]
    #     examples = extract_code(match, 'example')
    #     if len(examples) == 2 or len(examples) == 4 or len(examples) == 5 or len(examples) == 8 \
    #             or len(examples) == 9 or len(examples) == 10 or len(examples) == 18:
    #         # select a random example as the re-gen output
    #         index = random.randint(0, len(examples))
    #         res['code'] = examples[index]
    #         return res
    # return re_gen(origin_index)

    matches = extract_code(context)
    index = random.randint(0, len(matches) - 1)
    res['code'] = matches[index]
    return res


if __name__ == "__main__":
    re_gen(1)

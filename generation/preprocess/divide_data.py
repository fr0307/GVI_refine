import json
import random

from generation.config import origin_data, origin_vul_data


def divide():
    with open('../' + origin_data, 'r', encoding='utf-8') as f:
        data = json.load(f)

    vul_data = list(filter(lambda x: x['target'] == 1, data))

    random.shuffle(vul_data)

    with open('../' + origin_vul_data, 'w', encoding='utf-8') as f:
        json.dump(vul_data, f, indent=4)
        print('Data division succeed')


if __name__ == "__main__":
    divide()

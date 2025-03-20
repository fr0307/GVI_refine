import os
import xml.etree.ElementTree as ET
import re
import csv
import json
from collections import Counter
from io import StringIO

import matplotlib.pyplot as plt

from config import collected_raw_code_root, collected_original_raw_code_root, collected_refined_raw_code_root, analyze_result_original, analyze_result_refined, analyze_result_compare

severity_ignore_list = ['style', 'information']


def cppcheck(cppcheck_path=None, content=None, mode='file'):
    if mode == 'text':
        root = ET.fromstring(content)
    else:
        tree = ET.parse(cppcheck_path)
        root = tree.getroot()

    res = []
    for error in root.findall('.//error'):
        severity = error.get('severity')
        if severity in severity_ignore_list:
            continue
        first_location = error.find('location')
        file = first_location.get('file')
        res.append(int(re.split(r"[/\\.]", file)[-2]))
    return res


def flawfinder(flawfinder_path=None, content=None, mode='file'):
    res = []

    if mode == 'text':
        csv_reader = csv.DictReader(StringIO(content))
        for row in csv_reader:
            file = row.get('File')
            res.append(int(re.split(r"[/\\.]", file)[-2]))
    else:
        with open(flawfinder_path, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                file = row.get('File')
                res.append(int(re.split(r"[/\\.]", file)[-2]))

    return res


def analyze_original():
    file_num = len(os.listdir(collected_original_raw_code_root))
    res_list = [0 for _ in range(file_num)]

    cppcheck_path = os.path.join(collected_raw_code_root, 'cppcheck-original.xml')
    cppcheck_list = cppcheck(cppcheck_path, mode='file')
    counter = Counter(cppcheck_list)
    for index, count in counter.items():
        if 0 <= index < len(res_list):
            res_list[index] += count

    flawfinder_path = os.path.join(collected_raw_code_root, 'flawfinder-original.csv')
    flawfinder_list = flawfinder(flawfinder_path, mode='file')
    counter = Counter(flawfinder_list)
    for index, count in counter.items():
        if 0 <= index < len(res_list):
            res_list[index] += count

    with open(analyze_result_original, 'w', encoding='utf-8') as f:
        json.dump(res_list, f)

    count = 0
    for index in range(len(res_list)):
        if res_list[index] == 0:
            # print(index)
            count += 1
    print(f'original: total count {count} out of {len(res_list)}, FP rate: {count / len(res_list)}')


def analyze_refined():
    file_list = os.listdir(collected_refined_raw_code_root)
    file_num = len(file_list)
    file_index_list = [int(re.search(r'\d+', item).group()) for item in file_list]
    index_dict = {}
    for index, value in enumerate(sorted(file_index_list)):
        index_dict[value] = index
    res_list = [0 for _ in range(file_num)]

    cppcheck_path = os.path.join(collected_raw_code_root, 'cppcheck-refined.xml')
    cppcheck_list = cppcheck(cppcheck_path, mode='file')
    counter = Counter(cppcheck_list)
    for index, count in counter.items():
        if index in index_dict:
            res_list[index_dict[index]] += count

    flawfinder_path = os.path.join(collected_raw_code_root, 'flawfinder-refined.csv')
    flawfinder_list = flawfinder(flawfinder_path, mode='file')
    counter = Counter(flawfinder_list)
    for index, count in counter.items():
        if index in index_dict:
            res_list[index_dict[index]] += count

    with open(analyze_result_refined, 'w', encoding='utf-8') as f:
        json.dump(res_list, f)

    count = 0
    for index in range(len(res_list)):
        if res_list[index] == 0:
            # print(index)
            count += 1
    print(f'refined: total count {count} out of {len(res_list)}, FP rate: {count / len(res_list)}')

    return sorted(file_index_list)


def analyze_compare(file_index_list):
    with open(analyze_result_original, 'r', encoding='utf-8') as f:
        res_original = json.load(f)
    with open(analyze_result_refined, 'r', encoding='utf-8') as f:
        res_refined = json.load(f)
    for i in range(len(res_refined)):
        res_refined[i] -= res_original[file_index_list[i]]

    with open(analyze_result_compare, 'w', encoding='utf-8') as f:
        json.dump(res_refined, f)
    print('comparison done')


def plot_result():
    with open(analyze_result_original, 'r', encoding='utf-8') as f:
        res_original = json.load(f)
        range_original = range(min(res_original), max(res_original)+1)
        res_original_counter = [Counter(res_original).get(value, 0) for value in range_original]
    with open(analyze_result_refined, 'r', encoding='utf-8') as f:
        res_refined = json.load(f)
        range_refined = range(min(res_refined), max(res_refined)+1)
        res_refined_counter = [Counter(res_refined).get(value, 0) for value in range_refined]
    with open(analyze_result_compare, 'r', encoding='utf-8') as f:
        res_compared = json.load(f)
        range_compared = range(min(res_compared), max(res_compared)+1)
        res_compared_counter = [Counter(res_compared).get(value, 0) for value in range_compared]

    plt.figure(figsize=(8, 6))
    plt.bar(range_original, res_original_counter, color='skyblue')
    plt.xlabel('Vulnerability Number')
    plt.ylabel('Count')
    plt.title('Bar Chart of Original Data')
    plt.xticks(range_original)
    plt.savefig('./raw_code/bar_chart_original.png')
    plt.close()

    plt.figure(figsize=(8, 6))
    plt.bar(range_refined, res_refined_counter, color='red')
    plt.xlabel('Vulnerability Number')
    plt.ylabel('Count')
    plt.title('Bar Chart of Refined Data')
    plt.xticks(range_refined)
    plt.savefig('./raw_code/bar_chart_refined.png')
    plt.close()

    plt.figure(figsize=(8, 6))
    plt.bar(range_compared, res_compared_counter, color='green')
    plt.xlabel('Vulnerability Number')
    plt.ylabel('Count')
    plt.title('Bar Chart of Comparison')
    plt.xticks(range_compared)
    plt.savefig('./raw_code/bar_chart_compare.png')
    plt.close()

    print('plot done')


if __name__ == "__main__":
    analyze_original()
    file_index_list = analyze_refined()
    analyze_compare(file_index_list)
    plot_result()


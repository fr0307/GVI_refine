import subprocess
import json
import csv
import xml.etree.ElementTree as ET
from io import StringIO

from generation.config import rm_comments_output


temp_code_path = "./temp_code.c"

cppcheck_command = ['cppcheck', '--enable=all', '--xml']
flawfinder_command = ["flawfinder", "-m", "0", "--csv"]

severity_ignore_list = ['style', 'information']


def single_tool_analysis(code, tool_command):
    # 保存当前样本到临时文件temp.c
    with open(temp_code_path, 'w') as f:
        f.write(code)

    # 拼接完整命令
    command = tool_command + [temp_code_path]

    # 用subprocess模块执行命令，以静态分析工具对样本进行分析，返回结果
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        stdout = result.stdout
        stderr = result.stderr
        return {'stdout': stdout, 'stderr': stderr}
    except subprocess.CalledProcessError as e:
        print(f'Subcommand failed:\n{e}')
        return {}


def multi_tool_analysis(code):
    vul_count = 0

    # 调用cppcheck进行分析，分析结果包含在标准错误流中
    cppcheck_output = single_tool_analysis(code, cppcheck_command)
    cppcheck_res = cppcheck_output['stderr']

    if cppcheck_output['stdout'] == 'Checking temp_code.c ...\n':
        # 从标准错误中提取XML
        root = ET.fromstring(cppcheck_res)
        # 遍历每个<error>子标签，若没有被过滤，增加一个漏洞数量
        for error in root.findall('.//error'):
            severity = error.get('severity')
            # 特别地，过滤information和style等级，它们和漏洞无关
            if severity in severity_ignore_list:
                continue
            vul_count += 1

    # 调用flawfinder进行分析，分析结果包含在标准输出流中
    flawfinder_output = single_tool_analysis(code, flawfinder_command)
    flawfinder_res = flawfinder_output['stdout']

    if flawfinder_output['stderr'] == '':
        # 从标准输出中提取CSV
        csv_reader = csv.DictReader(StringIO(flawfinder_res))
        # 每一行代表一个漏洞，增加一个漏洞数量
        for row in csv_reader:
            vul_count += 1

    return vul_count


if __name__ == '__main__':
    with open('../' + rm_comments_output, encoding='utf-8') as f:
        original_dataset = json.load(f)

    for i in range(20):
        code = original_dataset[i]['code']
        print(multi_tool_analysis(code))
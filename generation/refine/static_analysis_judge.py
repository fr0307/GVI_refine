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
    with open(temp_code_path, 'w') as f:
        f.write(code)

    command = tool_command + [temp_code_path]

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

    cppcheck_output = single_tool_analysis(code, cppcheck_command)
    cppcheck_res = cppcheck_output['stderr']

    if cppcheck_output['stdout'] == 'Checking temp_code.c ...\n':
        root = ET.fromstring(cppcheck_res)
        for error in root.findall('.//error'):
            severity = error.get('severity')
            if severity in severity_ignore_list:
                continue
            vul_count += 1

    flawfinder_output = single_tool_analysis(code, flawfinder_command)
    flawfinder_res = flawfinder_output['stdout']

    if flawfinder_output['stderr'] == '':
        csv_reader = csv.DictReader(StringIO(flawfinder_res))
        for row in csv_reader:
            vul_count += 1

    return vul_count


if __name__ == '__main__':
    with open('../' + rm_comments_output, encoding='utf-8') as f:
        original_dataset = json.load(f)

    for i in range(20):
        code = original_dataset[i]['code']
        print(multi_tool_analysis(code))
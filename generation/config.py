import os

OPENAI_API_KEY = "sk-b3d83812ed3c4e348df3a79fd74a013f"

# MODEL = "gpt-4"
# MODEL = "qwen-turbo"
MODEL = "qwen-coder-turbo"
# MODEL = "qwen2.5-coder-7b-instruct"
# MODEL = "deepseek-r1"
# MODEL = "deepseek-v3"

BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# origin_data = 'origin_data_reveal/reveal.json'              # 存放原始数据: reveal 18169
origin_data = 'origin_data_devign/devign.json'                    # 存放原始数据: devign 27318
# origin_data = 'origin_data_bigvul/bigvul.json'                    # 存放原始数据: bigvul 188636

# origin_vul_data = 'origin_data_reveal/reveal_vul.json'            # 存放原始漏洞数据: reveal_vul 1664
origin_vul_data = 'origin_data_devign/devign_vul.json'            # 存放原始漏洞数据: devign_vul 12460
# origin_vul_data = 'origin_data_bigvul/bigvul_vul.json'            # 存放原始漏洞数据: bigvul_vul 10900

# gen_output_root = 'output_data_reveal/chain_reveal_gpt4'                               # 存放原始生成的文件
gen_output_root = 'output_data_devign/chain_devign_gpt4'                                 # 存放原始生成的文件
# gen_output_root = 'output_data_bigvul/chain_bigvul_gpt4'                                 # 存放原始生成的文件


gen_output_result_root = gen_output_root + '_result'                                    # 存放后续处理文件
gen_combine_output = os.path.join(gen_output_result_root, 'chain_combine.json')         # 存放合并后的文件
rm_comments_output = os.path.join(gen_output_result_root, 'chain_rm_comments.json')     # 存放去除注释后的文件

similarity_database_root = os.path.join(gen_output_result_root, 'db')                   # 存放相似度计算的数据库
similarity_output = os.path.join(gen_output_result_root, 'similarity.json')             # 存放相似度计算后的文件
similarity_output_graph = os.path.join(gen_output_result_root, 'similarity_hist.png')   # 存放相似度计算后的图


# chain_inputs = [
#     "\n```c\n{example0}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label0} \n"
#     "\n```c\n{example1}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label1} \n"
#     "\n```c\n{example2}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label2} \n"
#     "\n```c\n{example3}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label3} \n"
#     "\n```c\n{example4}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label4} \n"
#     "\n```c\n{code}\n```\nIs there a vulnerability in this code? Just answer yes or no \n"
# ]
# chain_inputs = [
#     "\n```c\n{example0}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label0} \n"
#     "\n```c\n{example1}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label1} \n"
#     "\n```c\n{example2}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label2} \n"
#     "\n```c\n{example3}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label3} \n"
#     "\n```c\n{example4}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label4} \n"
#     "\n```c\n{example5}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label5} \n"
#     "\n```c\n{example6}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label6} \n"
#     "\n```c\n{example7}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label7} \n"
#     "\n```c\n{example8}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label8} \n"
#     "\n```c\n{example9}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label9} \n"
#     "\n```c\n{code}\n```\nIs there a vulnerability in this code? Just answer yes or no \n"
# ]
# chain_inputs = [
#     "\n```c\n{example0}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label0} \n"
#     "\n```c\n{example1}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label1} \n"
#     "\n```c\n{example2}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label2} \n"
#     "\n```c\n{example3}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label3} \n"
#     "\n```c\n{example4}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label4} \n"
#     "\n```c\n{example5}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label5} \n"
#     "\n```c\n{example6}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label6} \n"
#     "\n```c\n{example7}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label7} \n"
#     "\n```c\n{example8}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label8} \n"
#     "\n```c\n{example9}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label9} \n"
#     "\n```c\n{example10}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label10} \n"
#     "\n```c\n{example11}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label11} \n"
#     "\n```c\n{example12}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label12} \n"
#     "\n```c\n{example13}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label13} \n"
#     "\n```c\n{example14}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label14} \n"
#     "\n```c\n{example15}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label15} \n"
#     "\n```c\n{example16}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label16} \n"
#     "\n```c\n{example17}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label17} \n"
#     "\n```c\n{example18}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label18} \n"
#     "\n```c\n{example19}\n```\n"
#     "Is there a vulnerability in this code? Just answer yes or no \n"
#     "{label19} \n"
#     "\n```c\n{code}\n```\nIs there a vulnerability in this code? Just answer yes or no \n"
# ]
# chain_inputs = [
#     "\n```c\n{code}\n```\nIs there a vulnerability in this code? Let's think step by step. Answer 'AI: yes' or 'AI: no' at last.\n"
# ]
# chain_inputs = [
#     "\n```c\n{code}\n```\nIs there a vulnerability in this code? Just answer yes or no \n"
# ]


chain_sys = "I need your help to generate some vulnerable C functions to train our ML model. Please using all your knowledge to follow the steps below.\n"


chain_inputs = [
    "\n```c\n{code}\n```\nStep 1: Application Scenario. Perform a general analysis of the application scenario of the given C language function example. Please limit your response to no more than 100 tokens. \n",

    "Step 2: Identify Vulnerability Type. Base on step 1, identify the type of security vulnerability present in the example function code. Please limit your response to no more than 100 tokens. \n",

    "Step 3: Extract Vulnerability Pattern. Base on step 2, extract the vulnerability pattern. Please limit your response to no more than 100 tokens.\n",

    "Step 4: Generate Similar Examples. Base on step 1 and step 3, create 4 independent and high-quality vulnerable functions similar to the example function's application scenario and vulnerability pattern. Please limit the response examples to no less than 800 tokens. \n",

]

# chain_inputs = [
#     "\n```c\n{code}\n```\nStep 1: Extract Vulnerability Pattern. Extract the vulnerability pattern. Please limit your response to no more than 100 tokens.\n",
#
#     "Step 2: Application Scenario. Perform a general analysis of the application scenario of the given C language function example. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 3: Identify Vulnerability Type. Identify the type of security vulnerability present in the example function code. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 4: Generate Similar Examples. Base on step 1 and step 2, create 4 independent and high-quality vulnerable functions similar to the example function's application scenario and vulnerability pattern. Please limit the response examples to no less than 800 tokens. \n",
#
# ]

# chain_inputs = [
#     "\n```c\n{code}\n```\nStep 1: Application Scenario. Perform a general analysis of the application scenario of the given C language function example. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 2: Extract Vulnerability Pattern. Extract the vulnerability pattern. Please limit your response to no more than 100 tokens.\n",
#
#     "Step 3: Identify Vulnerability Type. Identify the type of security vulnerability present in the example function code. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 4: Generate Similar Examples. Base on step 1 and step 2, create 4 independent and high-quality vulnerable functions similar to the example function's application scenario and vulnerability pattern. Please limit the response examples to no less than 800 tokens. \n",
#
# ]




# chain_inputs = [
#     "\n```c\n{code}\n```\nStep 1: Identify Vulnerability Type. Identify the type of security vulnerability present in the example function code. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 2: Extract Vulnerability Pattern. Extract the vulnerability pattern. Please limit your response to no more than 100 tokens.\n",
#
#     "Step 3: Application Scenario. Perform a general analysis of the application scenario of the given C language function example. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 4: Generate Similar Examples. Base on step 2 and step 3, create 4 independent and high-quality vulnerable functions similar to the example function's application scenario and vulnerability pattern. Please limit the response examples to no less than 800 tokens. \n",
#
# ]

# chain_inputs = [
#     "\n```c\n{code}\n```\nStep 1: Identify Vulnerability Type. Identify the type of security vulnerability present in the example function code. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 2: Application Scenario. Perform a general analysis of the application scenario of the given C language function example. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 3: Extract Vulnerability Pattern. Base on step 1, extract the vulnerability pattern. Please limit your response to no more than 100 tokens.\n",
#
#     "Step 4: Generate Similar Examples. Base on step 2 and step 3, create 4 independent and high-quality vulnerable functions similar to the example function's application scenario and vulnerability pattern. Please limit the response examples to no less than 800 tokens. \n",
#
# ]

# chain_inputs = [
#     "\n```c\n{code}\n```\nStep 1: Extract Vulnerability Pattern. Extract the vulnerability pattern. Please limit your response to no more than 100 tokens.\n",
#
#     "Step 2: Identify Vulnerability Type. Identify the type of security vulnerability present in the example function code. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 3: Application Scenario. Perform a general analysis of the application scenario of the given C language function example. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 4: Generate Similar Examples. Base on step 1 and step 3, create 4 independent and high-quality vulnerable functions similar to the example function's application scenario and vulnerability pattern. Please limit the response examples to no less than 800 tokens. \n",
#
# ]

# chain_inputs = [
#     "This is input NO.{code}. Please create 8 independent and vulnerable C functions as the given example. Please split each example with //Example 0. \n"
# ]

# chain_inputs = [
#     "\n```c\n{code}\n```\nPlease create 8 independent and vulnerable functions as the given example. Please split each example with //Example 0. \n"
# ]

# chain_inputs = [
#     "\n```c\n{code}\n```\nStep 1: Identify Vulnerability Type. Identify the type of security vulnerability present in the example function code. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 2: Extract Vulnerability Pattern. Base on step 1, extract the vulnerability pattern. Please limit your response to no more than 100 tokens.\n",
#
#     "Step 3: Generate Similar Examples. Base on step 2, create 8 independent and vulnerable functions similar to the example function's vulnerability pattern. Please split each example with //Example 0. \n",
#
# ]

# chain_inputs = [
#     "\n```c\n{code}\n```\nStep 1: Application Scenario. Perform a general analysis of the application scenario of the given C language function example. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 2: Extract Vulnerability Pattern. Extract the vulnerability pattern. Please limit your response to no more than 100 tokens.\n",
#
#     "Step 3: Generate Similar Examples. Create 8 independent and vulnerable functions similar to the example function's vulnerability pattern. Please split each example with //Example 0. \n",
#
# ]

# chain_inputs = [
#     "\n```c\n{code}\n```\nStep 1: Application Scenario. Perform a general analysis of the application scenario of the given C language function example. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 2: Identify Vulnerability Type. Identify the type of security vulnerability present in the example function code. Please limit your response to no more than 100 tokens. \n",
#
#     "Step 3: Generate Similar Examples. Create 8 independent and vulnerable functions similar to the example function. Please split each example with //Example 0. \n",
#
# ]
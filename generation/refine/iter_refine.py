from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, \
    SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
import os
import re

from config import gen_refine_output_root, gen_final_output_root
from generation.config import MODEL, BASE_URL
import prompts


def get_output_path(dir, index, file_name):
    if not os.path.exists(dir):
        os.mkdir(dir)
    output_dir = os.path.join(dir, str(index))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_path = os.path.join(output_dir, file_name)
    return output_path


def refine(code, suggestion, index, iteration, step):
    # 初始化大模型对话对象
    chat = ChatOpenAI(
        model_name=MODEL,
        streaming=True,
        temperature=.9,
        base_url=BASE_URL
    )
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(prompts.refine_system),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=chat, verbose=False)

    # 拼接对5个维度含义的解释内容
    target_areas = "\n".join(prompts.factor_explanations)
    step += 1

    # 同大模型进行对话，令其将建议内容应用至原始样本，改进其质量
    conversation.predict(input=prompts.refine_prompt.format(step=step, code=code, suggestion=suggestion, areas=target_areas))

    # 保存Refine模块对话内容到文件
    refine_file_path = get_output_path(gen_refine_output_root, index, f"{index}_iter{iteration}.c")
    with open(refine_file_path, 'w', encoding="utf-8") as f:
        f.write(memory.buffer_as_str)

    last_answer = memory.chat_memory.messages[-1].content
    memory.clear()

    # 提取改进后样本
    code_reg = r'```c\n(.+?)\n```'
    try:
        matches = re.findall(code_reg, last_answer, re.DOTALL)
        if not matches:
            refined_code = ""
        else:
            refined_code = matches[-1]
    except re.error as e:
        refined_code = ""

    return refined_code


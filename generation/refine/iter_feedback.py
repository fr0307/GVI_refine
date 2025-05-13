from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, \
    SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
import re
import os

from config import gen_feedback_root, gen_final_output_root, early_stop_rate_reg, early_stop_msg_reg, areas
from generation.config import MODEL, BASE_URL
import prompts


def get_output_path(index, file_name):
    if not os.path.exists(gen_feedback_root):
        os.mkdir(gen_feedback_root)
    output_dir = os.path.join(gen_feedback_root, str(index))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_path = os.path.join(output_dir, file_name)
    return output_path


def feedback(code, index, iteration):
    # 初始化大模型对话对象
    chat = ChatOpenAI(
        model_name=MODEL,
        streaming=True,
        temperature=.9,
        base_url=BASE_URL
    )
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(prompts.feedback_system),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=chat, verbose=False)

    # 初始化局部变量
    early_stop_flag = True
    step = 2

    # 第一阶段对话，令大模型理解样本代码
    conversation.predict(input=prompts.explain_prompt.format(code=code))

    # 第二阶段对话，令大模型就5个质量维度分别对样本代码进行评估、评分
    for quality_feedback_index, quality_feedback_prompt in enumerate(prompts.quality_feedback_prompts):
        conversation.predict(input=quality_feedback_prompt.format(step=step))
        # 对每个维度的评价，以正则式判断其是否同时含有两个“早停正则”包含的内容，据此设置早停标签
        quality_feedback = memory.chat_memory.messages[-1].content
        if not re.search(early_stop_rate_reg.format(area=re.escape(areas[quality_feedback_index])), quality_feedback) \
                or not re.search(early_stop_msg_reg, quality_feedback):
            early_stop_flag = False
        step += 1

    # 第三阶段对话，若没有早停，继续指引大模型对评估结果进行总结，并据此给出质量提升建议
    if not early_stop_flag:
        possible_methods = "\n".join(prompts.quality_refine_prompts)
        conversation.predict(input=prompts.feedback_prompt.format(step=step, methods=possible_methods))

    # 保存Suggestion模块对话内容到文件
    file_path = get_output_path(index, f"{index}_iter{iteration}.c")
    with open(file_path, 'w', encoding="utf-8") as f:
        f.write(memory.buffer_as_str)

    last_answer = memory.chat_memory.messages[-1].content
    memory.clear()
    return last_answer, step, early_stop_flag

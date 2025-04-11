from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, \
    SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
import re
import os

from config import gen_feedback_root, early_stop_reg, areas
from generation.config import MODEL, BASE_URL
import prompts
from static_analysis_judge import multi_tool_analysis


def get_output_path(index, file_name):
    if not os.path.exists(gen_feedback_root):
        os.mkdir(gen_feedback_root)
    output_dir = os.path.join(gen_feedback_root, str(index))
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_path = os.path.join(output_dir, file_name)
    return output_path


def feedback(code, index, iteration):
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

    early_stop_flag = True
    step = 2

    conversation.predict(input=prompts.judge_prompts[0].format(code=code))

    for quality_feedback_index, quality_feedback_prompt in enumerate(prompts.quality_feedback_prompts):
        conversation.predict(input=quality_feedback_prompt.format(step=step))
        quality_feedback = memory.chat_memory.messages[-1].content
        if not re.search(early_stop_reg.format(area=re.escape(areas[quality_feedback_index])), quality_feedback):
            early_stop_flag = False
        step += 1

    if not early_stop_flag:
        possible_methods = "\n".join(prompts.quality_refine_prompts)
        conversation.predict(input=prompts.feedback_prompt.format(step=step, methods=possible_methods))

    file_path = get_output_path(index, f"{index}_iter{iteration}.c")
    with open(file_path, 'w', encoding="utf-8") as f:
        f.write(memory.buffer_as_str)

    last_answer = memory.chat_memory.messages[-1].content
    memory.clear()
    return last_answer, step, early_stop_flag

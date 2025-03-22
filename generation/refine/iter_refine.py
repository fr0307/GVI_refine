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


def refine(code, index, iteration, memory, step):
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
    # memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=chat, verbose=False)

    # target_areas = "\n".join(prompts.factor_explanations)
    possible_methods = "\n".join(prompts.quality_refine_prompts)
    step += 1
    conversation.predict(input=prompts.refine_prompt.format(step=step, code=code, methods=possible_methods))

    refine_file_path = get_output_path(gen_refine_output_root, index, f"{index}_iter{iteration}.c")
    with open(refine_file_path, 'w', encoding="utf-8") as f:
        f.write(memory.buffer_as_str)

    last_answer = memory.chat_memory.messages[-1].content
    memory.clear()

    code_reg = r'```c\n(.+?)\n```'
    matches = re.findall(code_reg, last_answer, re.DOTALL)
    refined_code = matches[-1]

    final_file_path = get_output_path(gen_final_output_root, index, f"{index}.c")
    with open(final_file_path, 'w', encoding="utf-8") as f:
        f.write(refined_code)

    return refined_code


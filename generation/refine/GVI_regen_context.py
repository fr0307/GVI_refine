from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, \
    SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
import re
import json
import os

from generation.config import chain_sys, chain_inputs, MODEL, BASE_URL, origin_vul_data, OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def re_gen_context(origin_index):
    with open('../' + origin_vul_data, 'r') as f:
        origin_dataset = json.load(f)
        origin_code = origin_dataset[origin_index]['func']

    context = gen(origin_code)

    matches = extract_code(context)
    if len(matches) == 4:
        return context

    # sth goes wrong, re-gen again
    return re_gen_context(origin_index)


def gen(code):
    chat = ChatOpenAI(
        model_name=MODEL,
        streaming=True,
        temperature=.9,
        base_url=BASE_URL
    )

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(chain_sys),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=chat, verbose=False)

    for chain_input in chain_inputs:
        conversation.predict(input=chain_input.format(code=code))

    res = memory.buffer_as_str
    memory.clear()

    return res


def extract_code(context):
    code_pattern = r'```c(.+?)```'
    matches = re.findall(code_pattern, context, re.DOTALL)

    return matches[-(len(matches) - 1):] if len(matches) == 5 else []

# def extract_code(context, mode):
#     matches = []
#     if mode == 'text':
#         pattern = r'```c\n(.+?)\n```'
#         matches = re.findall(pattern, context, re.DOTALL)
#     elif mode == 'example':
#         match_list = [
#             "// Example \d+",
#             "//Example \d+",
#             "// Example Function \d+",
#             "// Example Vulnerable Function \d+",
#             "// \d+. Example",
#             "// Function \d+",
#             "// vulnerable function \d+",
#             "// Vulnerable function \d+",
#             "// Vulnerable function \#\d+",
#             "// Vulnerable functions example \d+",
#             "// Vulnerable Function \d+",
#             "// Vulnerable function example \d+",
#             "// Vulnerable Function Example \d+",
#             "// \d+. Vulnerable Function",
#             "// Vulnerable example \d+",
#             "// Vulnerable Example \d+",
#             "// Vulnerable C Function Example \d+",
#             "// Similar Example \d+",
#             "/\* Example \d+ \*/",
#             "/\* Example \d+: .*? \*/",
#             "/\* Vulnerable Function \d+ \*/",
#             "/\* Vulnerable Function \d+: .*? \*/",
#             "/\* Vulnerable function \d+: .*? \*/",
#             "/\* Vulnerable function example \d+ .*?\*/",
#             "/\* Vulnerable Function Example \d+ .*?\*/",
#             "/\*.*?Function \d+: .*? \*/",
#             "/\*.*?Example \d+: .*? \*/",
#         ]
#         for match in match_list:
#             pattern = rf'{match}.*?\n(.*?)(?={match}|\Z)'
#
#             tmp_matches = re.findall(pattern, context, re.DOTALL)
#             if len(tmp_matches) > 0:
#                 matches = tmp_matches
#                 break
#
#     return matches

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, \
    SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
import re
import os

from config import gen_feedback_root, judge_reg
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


def judge_vulnerable(code):
    # 调用静态分析，检查当前样本中的总漏洞数
    vul_num = multi_tool_analysis(code)

    # 若无漏洞返回false，否则返回true
    if vul_num <= 0:
        vul_judge = False
    else:
        vul_judge = True

    return vul_judge

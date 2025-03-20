feedback_system = "I am building a dataset of vulnerable functions. You are an advisor, and you need to offer some feedbacks to help turn the provided function into a high-quality sample of vulnerable functions. Please use your background knowledge to follow the steps below.\n\n"

judge_prompts = ["Step 1: explain the given function. Please read and understand the function provided below, then summarize its meaning and functionality. Your answer should be within 100 tokens."\
            "\n[function]\n```c\n{code}\n```",
                 "Step 2: determine whether there are certain types of vulnerabilities. The given function above may contain vulnerabilities or may not. "
            "Below, I will give descriptions of certain types of vulnerabilities, "
            "please determine whether the given function contains vulnerabilities that correspond to these descriptions." \
            " If it does, start your answer with `Yes, it contains such kind of vulnerabilities`, then identify the type and location of the " \
            "vulnerability. Otherwise, start the answer with `No, it doesn't contain such vulnerabilities`, then briefly explain why."\
            " Note: It is acceptable for the function to have other types of vulnerabilities not listed in the provided vulnerability type descriptions." \
            " The focus is on the types of vulnerabilities described below. The function does not need to contain all the described vulnerabilities; identifying even a subset of them is sufficient." \
            " Other aspects, such as the names of identifiers, are not important."\
            " Your answer should be within 100 tokens. "\
            "\n[vulnerability type descriptions]\n{type}\n\n"
]


factor_explanations = [
    "'Complexity' refers specifically to how intricate or convoluted the parts containing vulnerabilities are, rather than the overall complexity of the entire code snippet.",
    "'Completeness' means that the function includes all its original content without omitting any parts using ellipses or other similar methods.",
    "'Relevance' the degree of association between the function content and its primary task.",
    "'Domain-Specificity' refers to the degree to which the function is tailored to a particular domain or application context."
    "'Single-Function Enclosure' refers to the extent to which all logic is encapsulated within a single function. While function calls are allowed within this function, no additional function definitions (i.e., function bodies) should appear in the code. Additionally, global variables and macro definitions (e.g., #define) should be avoided unless they are necessary and placed inside the function."
]

quality_improvement_prompts = [
    "Step {step}: Assess Complexity. Here, 'Complexity' refers specifically to how intricate or convoluted the parts containing vulnerabilities are, rather than the overall complexity of the entire code snippet. You can evaluate complexity based on:\n1-The number of lines\n2-Cyclomatic complexity\n3-Other reasonable metrics\nPlease review the given function and provide your assessment of the complexity of the vulnerable parts. Your answer should be within 100 tokens.\n\n",
    "Step {step}: Assess Completeness. Here 'Completeness' means that the function includes all its original content without omitting any parts using ellipses or other similar methods. Please review the given function and provide your assessment of its completeness. Your answer should be within 100 tokens.\n\n",
    "Step {step}: Assess Relevance. Here 'Relevance' means the degree of association between the function content and its primary task. You may evaluate relevance based on:\n1-The number of lines of code unrelated to task\n2-Percentage of code related to task\n3-Other reasonable metrics.\nPlease review the given function and provide your assessment of its completeness. Your answer should be within 100 tokens.\n\n",
    "Step {step}: Assess Domain-Specificity. Here, 'Domain-Specificity' refers to the degree to which the function is tailored to a particular domain or application context. You can evaluate domain-specificity based on:\n1-The relevance of identifier names to the domain\n2-The presence of Common Weakness Enumeration (CWE) entries relevant to the domain\n3-Other reasonable metrics\nPlease review the given function and provide your assessment of its domain-specificity. Your answer should be within 100 tokens.\n\n",
    "Step {step}: Assess Single-Function Enclosure. Here, 'Single-Function Enclosure' refers to the extent to which all logic is encapsulated within a single function. While function calls are allowed within this function, no additional function definitions (i.e., function bodies) should appear in the code. Additionally, global variables and macro definitions (e.g., #define) should be avoided unless they are necessary and placed inside the function. You can evaluate single-function enclosure based on:\n1-Whether the code contains more than one function body\n2-Whether the code contains global variables or macro definitions (e.g., #define) outside the function.\n3-Other reasonable metrics.\nPlease review the given function and provide your assessment of its single-function enclosure. Your answer should be within 100 tokens.\n\n"
]

feedback_prompt = "Step {step}: Summarize and Provide Feedback. Based on your assessments in Steps 3-6, summarize the evaluations you have made and provide feedback on how to refine the provided code to improve its quality in the areas assessed. "\
    "Specifically, if you believe the provided function already performs well in these areas, simply respond with `I think the code does not need improvement.`. "\
    "Note that we are building a single high-quality vulnerable function sample. Therefore, do not try to fix any vulnerabilities in the given function. Additionally, do not add extra functions into existing code." \
    "Your answer should be within 150 tokens.\n\n"

refine_system = "I am building a dataset of vulnerable functions. You are an assistant, and yout need to help me refine the provided function, make it a high-quality sample of vulnerable function. Please use all your background knowledge to help me.\n\n"

refine_prompt = "I've recieved some feedbacks about the provided function below, please help me refine the function based on that feedback to improve its quality in the target areas given below." \
                " Please provide the complete function after refine in the following format: ```c //(function after refine) ```." \
                " Remember we are building a high-quality vulnerable function sample. Therefore, do not try to fix any vulnerabilities in the given function. Additionally, do not add extra functions into existing code." \
                "\n[function]\n```c\n{code}\n```\n[feedback]\n{feedback}\n[target areas]\n{areas}\n"

inject_system = "I am building a dataset of vulnerable functions. Your task is to assist me in creating high-quality vulnerable function samples by injecting specific types of vulnerabilities into the provided functions. The goal is to introduce vulnerabilities rather than fix existing ones. Additionally, do not add extra functions into existing code. Please use your expertise and background knowledge to help me in this process.\n\n"

inject_prompts = [
    "Step 1: explain the given function. Please read and understand the function provided below, then summarize its meaning and functionality. Your answer should be within 100 tokens."
    "\n[function]\n```c\n{code}\n```",
    "Step 2: inject vulnerabilities. The given code lacks certain types of vulnerabilities. You will be provided with descriptions of these vulnerabilities. "
    "Remember, your task is to inject these vulnerabilities into the function above, not to fix them. "
    "Please modify the function above to inject these vulnerabilities, making it a high-quality vulnerable function sample. "
    "You may achieve this by:\n1-Replacing existing correct parts with equivalent logic that introduces vulnerabilities.\n2-Adding new parts with vulnerabilities that relate to the existing function logic.\n3-Using other reasonable methods. "
    "Please provide the complete function after injection in the following format: ```c //(function after injection) ```. Your answer should be within 125 tokens. "
    "\n[vulnerability type descriptions]\n{type}\n\n"
]
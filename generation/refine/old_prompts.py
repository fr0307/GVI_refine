# judge_prompt = "```c\n{code}\n```\nStep 1: determine whether there are certain types of vulnerabilities: The code above may " \
#                "contain vulnerabilities or may not. Please determine whether the code contains vulnerabilities of the type described by the pattern." \
#                " If it does,start your answer with `Yes, it contains such kind of vulnerabilities`, then identify the type and location of the " \
#                "vulnerability. Otherwise, start the answer with `No, it doesn't contain such vulnerabilities`, then indicate where in the code a " \
#                "vulnerability of the type described by the pattern could be introduced. Your answer should be within 100 tokens.\nThe pattern is:\n" \
#                "{pattern}\n\n"


# quality_improvement_prompts = [
#     "Step 3: Increase complexity. Real-world vulnerabilities often involve multiple lines of code. If the existing vulnerabilities in the code consist of only a single line, provide your advise on how to expand them to make the vulnerabilities more complex and span multiple lines of code. Your answer should be within 100 tokens.\n\n",
#     "Step 4: Increase completeness. Completeness indicates that a code snippet contains all its original content without omitting any parts using ellipses or similar methods. If the provided code has completeness issues, please offer suggestions on how to complete the omitted parts to enhance its completeness. Your answer should be within 100 tokens.\n\n"
# ]

# quality_feedback_prompts = [
#     "Step {step}: Assess Complexity. Here, 'Complexity' refers to how intricate or convoluted the vulnerable parts are. A higher score means the vulnerable code is deeply embedded within complex logic (e.g., multiple layers of indirection, nested structures, or intertwined control flows), making it harder to analyze but still exploitable. The goal is to assess how much additional complexity surrounds the vulnerable logic, not the overall function size. You can evaluate complexity based on:\n1-The number of lines\n2-Cyclomatic complexity\n3-Other reasonable metrics\nPlease review the given function and provide your assessment of the complexity of the vulnerable parts. Your answer should be within 100 tokens.\n\n",
#     "Step {step}: Assess Completeness. Here 'Completeness' means that the function includes all its original content without omitting any parts using ellipses or other similar methods. Please review the given function and provide your assessment of its completeness. Your answer should be within 100 tokens.\n\n",
#     "Step {step}: Assess Relevance. Here 'Relevance' means the degree of association between the function content and its primary task. You may evaluate relevance based on:\n1-The number of lines of code unrelated to task\n2-Percentage of code related to task\n3-Other reasonable metrics.\nPlease review the given function and provide your assessment of its completeness. Your answer should be within 100 tokens.\n\n",
#     "Step {step}: Assess Domain-Specificity. Here, 'Domain-Specificity' refers to the degree to which the function is tailored to a particular domain or application context. You can evaluate domain-specificity based on:\n1-The relevance of identifier names to the domain\n2-The presence of Common Weakness Enumeration (CWE) entries relevant to the domain\n3-Other reasonable metrics\nPlease review the given function and provide your assessment of its domain-specificity. Your answer should be within 100 tokens.\n\n",
#     "Step {step}: Assess Single-Function Enclosure. Here, 'Single-Function Enclosure' refers to the extent to which all logic is encapsulated within a single function. While function calls are allowed within this function, no additional function definitions (i.e., function bodies) should appear in the code. Additionally, global variables and macro definitions (e.g., #define) should be avoided unless they are necessary and placed inside the function. You can evaluate single-function enclosure based on:\n1-Whether the code contains more than one function body\n2-Whether the code contains global variables or macro definitions (e.g., #define) outside the function.\n3-Other reasonable metrics.\nPlease review the given function and provide your assessment of its single-function enclosure. Your answer should be within 100 tokens.\n\n"
# ]

# feedback_prompt = "Step {step}: Summarize and Provide Feedback. Based on your understanding and assessments of the function in Steps above, summarize the evaluations you have made and provide feedback on how to refine the provided code to improve its quality in the areas assessed."\
#     " Below you will be given some possible methods to improve the function quality in the target areas. You may refer to these suggestions to build your feedback or use your own reasonable methods."\
#     " Specifically, if you believe the provided function already performs well in these areas, or you cannot find ways to improve the function, simply respond with `I think the code does not need improvement.`."\
#     "\nNote:\n1-We are building a high-quality vulnerable function sample. Therefore, do not fix any vulnerabilities in the given function. Instead, you are welcome to introduce new vulnerabilities that are relevant to the function's domain and enhance its realism.\n2-Focus on improving the existing function. Do not add extra functions into the existing code.\n3-There is no need to add comments as part of the refinement.\n" \
#     "Your answer should be within 150 tokens.\n"\
#     "\n[possible methods]\n{methods}\n"


# feedback_prompts = [
#     "Base on Step 1, provide your feedback on how to introduce a vulnerability of the type described by the pattern at an appropriate location. "\
#     "Your answer should be within 125 tokens.\n\n",
#     "Base on the former Steps, summarize your feedback in how to refine the provided code to make the existing vulnerabilities more complex. "\
#     "Specifically, if you think the provided code does not need further improvement, simply respond with `I think the code is already perfect.`. "\
#     "Your answer should be within 125 tokens.\n\n"
# ]

# feedback_prompt = "Base on the former Steps, summarize your feedback in how to refine the provided code to make the existing vulnerabilities more complex. "\
#     "Specifically, if you think the provided code does not need further improvement, simply respond with `I think the code is already perfect.`. "\
#     "Your answer should be within 125 tokens.\n\n"

# refine_system = "I am building a dataset of vulnerable functions. You are an assistant, and yout need to help me refine the provided function, make it a high-quality sample of vulnerable function. Please use all your background knowledge to help me.\n\n"
#
# refine_prompt = "I've recieved some feedbacks about the provided function below, please help me refine the function based on that feedback to improve its quality in the target areas given below." \
#                 " Please provide the complete function after refine in the following format: ```c //(function after refine) ```." \
#                 " Remember we are building a high-quality vulnerable function sample. Therefore, do not try to fix any vulnerabilities in the given function. Additionally, do not add extra functions into existing code." \
#                 "\n[function]\n```c\n{code}\n```\n[feedback]\n{feedback}\n[target areas]\n{areas}\n"

# refine_prompt = "Step {step}: Refine the Function. Based on the feedback provided in the previous conversation, help me refine the function to improve its quality in the target areas mentioned. The definitions of these target areas can be found in the assessment part of our conversation above." \
#                 " In the feedback step above you were provided with some possible methods to improve the function quality in the target areas. You may refer to these suggestions or use your own reasonable methods."\
#                 " Please provide the complete function after refine in the following format: ```c //(function after refine) ```." \
#                 "\nNote:\n1-We are building a high-quality vulnerable function sample. Therefore, do not fix any vulnerabilities in the given function. Instead, you are welcome to introduce new vulnerabilities that are relevant to the function's domain and enhance its realism.\n2-Focus on improving the existing function. Do not add extra functions into the existing code.\n3-There is no need to add comments as part of the refinement.\n" \
#                 "\n[function]\n```c\n{code}\n```\n"

# inject_prompts = [
#     "Step 1: explain the given function. Please read and understand the function provided below, then summarize its meaning and functionality. Your answer should be within 100 tokens."
#     "\n[function]\n```c\n{code}\n```",
#     "Step 2: inject vulnerabilities. The given code lacks certain types of vulnerabilities. You will be provided with descriptions of these vulnerabilities. "
#     "Remember, your task is to inject these vulnerabilities into the function above, not to fix them. "
#     "Please modify the function above to inject these vulnerabilities, making it a high-quality vulnerable function sample. "
#     "You may achieve this by:\n1-Replacing existing correct parts with equivalent logic that introduces vulnerabilities.\n2-Adding new parts with vulnerabilities that relate to the existing function logic.\n3-Using other reasonable methods. "
#     "Please provide the complete function after injection in the following format: ```c //(function after injection) ```. Your answer should be within 125 tokens. "
#     "\n[vulnerability type descriptions]\n{type}\n\n"
# ]
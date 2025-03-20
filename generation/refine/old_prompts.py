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
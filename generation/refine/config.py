from generation.config import gen_output_root

cur_gen_output_root = '../' + gen_output_root
pattern_output = cur_gen_output_root + '_pattern/patterns.json'
type_output = cur_gen_output_root + '_type/types.json'
gen_feedback_root = cur_gen_output_root + '_feedback'
gen_refine_output_root = cur_gen_output_root + '_refine'
gen_final_output_root = cur_gen_output_root + '_final'
gen_extracted_output_root = cur_gen_output_root + '_extracted'
gen_discarded_output_root = cur_gen_output_root + '_discarded'

collected_raw_code_root = 'raw_code'
collected_original_raw_code_root = collected_raw_code_root + '/original'
collected_refined_raw_code_root = collected_raw_code_root + '/refined'

analyze_result_original = collected_raw_code_root + '/analyze-original.json'
analyze_result_refined = collected_raw_code_root + '/analyze-refined.json'
analyze_result_compare = collected_raw_code_root + '/analyze-compare.json'

MAX_ITER_NUM = 3

judge_reg = r"No, it doesn't contain such vulnerabilities"
early_stop_reg = r"\*\*{area} Rating\*\* 5"
areas = ['Complexity', 'Completeness', 'Relevance', 'Domain-Specificity', 'Single-Function Enclosure']


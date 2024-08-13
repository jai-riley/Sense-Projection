from align_tokens_to_gold import create_carried_sheet
from filter import filter
from tsv_to_key import process_tsv
from Scorer import calculate_scores
from combine_WSD_pipeline import combine_with_WSD

language = "Farsi"
lang_code = "FAR"
filter_POS = False
filter_BabelNet = False
filter_PanLex = True
add_WSD = False

print(language)
# Filter Settings
# file_aligned = f'../../data/{language}/second-sense/tokens-aligned-{language}.tsv'
file_BabelNet = f'../../data/{language}/new_format/problem-alignments-{language}-BabelNet.tsv'
# file_PanLex = f'../../data/{language}/new_format/problem-alignments-{language}-PanLex.tsv'
# file_filter_output = f'../../data/{language}/second-sense/filtered-tokens-aligned-{language}.tsv'
file_PanLex = f'/Users/jairiley/Desktop/Research/Sense-Projection/data/Farsi/problem-alignments-Farsi-Panlex.tsv'
#
file_aligned = f'../../data/{language}/tokens-aligned-{language}.tsv'
file_filter_output = f'../../data/{language}/filtered-tokens-aligned-{language}.tsv'

# Gold Alignment Settings
# file_gold_tokens = f'../../data/{language}/second-sense/tokens-gold-{language}.tsv'
# file_output_aligned = f'../../data/{language}/second-sense/{language}-carried-senses.tsv'

file_gold_tokens = f'../../data/{language}/gold-tokens-{language}.tsv'
file_output_aligned = f'../../data/{language}/{language}-carried-senses.tsv'

# Add WSD
WSD_system = "AMuSE"
# path_WSD = f"../../data/{language}/new_format/aligned-tokens-WSD-{language}.tsv"
path_WSD = f"../../data/{language}/aligned-tokens-WSD-{language}.tsv"

# Tokens to key files
# file_key_output = f'../../data/{language}/second-sense/silver-key-{language}.txt'
file_key_output = f'../../data/{language}/silver-key-{language}.txt'

# # Evaluate
# gold_key_file = f'../../data/{language}/second-sense/xl-wsd-key-{language}2.txt'
# silver_key_file = f'../../data/{language}/second-sense/silver-key-{language}.txt'
gold_key_file = f'../../data/{language}/Gold-key-{language}.txt'
silver_key_file = f'../../data/{language}/silver-key-{language}.txt'

# Run Code
if filter_BabelNet:
    if filter_PanLex:
        print("Filtered with BabelNet and PanLex")
    else:
        print("Filtered with BabelNet only")
elif filter_PanLex:
    print("Filtered with PanLex only")
elif filter_POS:
    print("Filtered POS only")

filter(file_aligned,
       file_BabelNet,
       file_PanLex,
       file_filter_output,
       lang_code,
       filter_BabelNet,
       filter_PanLex,
       filter_POS)

create_carried_sheet(file_filter_output,
                     file_gold_tokens,
                     file_output_aligned,
                     lang_code)
if add_WSD:
    print(f"Combined with Automatic WSD System: {WSD_system}")
    combine_with_WSD(path_WSD,
                     file_output_aligned)

process_tsv(file_output_aligned,
            file_key_output)

d_pipe = calculate_scores(gold_key_file,
                 silver_key_file)

# process_tsv(f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/aligned-tokens-WSD-{language}.tsv",
#             f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/WSD-key-{language}.txt")
#
# d_wsd = calculate_scores(gold_key_file,
#                  f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/WSD-key-{language}.txt")
#

# d_wsd = calculate_scores(f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/second-sense/xl-wsd-key-{language}2.txt",
#                  f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/new_format/test-{lang_code.lower()}.predictions.txt")
# d_wsd = calculate_scores(f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/second-sense/xl-wsd-key-{language}2.txt",
#                  f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/second-sense/silver-key-{language}2.txt")

# d_wsd = calculate_scores(f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/new_format/xl-wsd-key-{language}2.txt",
#                  f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/new_format/silver-key-{language}2.txt")

correct_same = 0
incorrect_same = 0
amuse_only_correct = 0
pipe_only_correct = 0
amuse_no_answer_pipe_correct = 0
amuse_incorrect_pipe_no_answer = 0
pipe_no_answer_amuse_correct = 0
pipe_incorrect_amuse_no_answer = 0
both_no_answer = 0


for key in d_pipe.keys():
    if d_pipe[key] == 1:
        if d_wsd[key] == 1:
            correct_same += 1
        elif d_wsd[key] == 0:
            pipe_only_correct += 1
        else:
            amuse_no_answer_pipe_correct += 1
    elif d_wsd[key] == 1:
        if d_pipe[key] == 0:
            amuse_only_correct += 1
        else:
            pipe_no_answer_amuse_correct += 1
    elif d_pipe[key] == -1:
        if d_wsd[key] == 0:
            amuse_incorrect_pipe_no_answer += 1
        else:
            both_no_answer += 1
    elif d_wsd[key] == -1:
        if d_pipe[key] == 0:
            pipe_incorrect_amuse_no_answer += 1
    elif d_pipe[key] == 0 and d_wsd[key] == 0:
        incorrect_same += 1

print(f"{correct_same}\t{pipe_only_correct}\t{amuse_no_answer_pipe_correct}")
print(f"{amuse_only_correct}\t{incorrect_same}\t{pipe_incorrect_amuse_no_answer}")
print(f"{pipe_no_answer_amuse_correct}\t{amuse_incorrect_pipe_no_answer}\t{both_no_answer}")
# Italian
# Both Correct: 383
# Pipe Correct Only: 166
# AMuSE Correct Only: 263
# Both Incorrect: 286
print(correct_same+pipe_only_correct+amuse_no_answer_pipe_correct+amuse_only_correct
      +incorrect_same+pipe_incorrect_amuse_no_answer+pipe_no_answer_amuse_correct+amuse_incorrect_pipe_no_answer+both_no_answer)

#

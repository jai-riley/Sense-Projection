from align_tokens_to_gold import create_carried_sheet
from filter import filter
from tsv_to_key import process_tsv
from Scorer import calculate_scores
from combine_WSD_pipeline import combine_with_WSD

language = "Spanish"
lang_code = "ES"
filter_POS = True
filter_BabelNet = True
filter_PanLex = True
add_WSD = False

print(language)
# Filter Settings
file_aligned = f'../../data/{language}/New_Ids/tokens-aligned-{language}.tsv'
file_BabelNet = f'../../data/{language}/New_Ids/problem-alignments-{language}-BabelNet.tsv'
file_PanLex = f'../../data/{language}/New_Ids/problem-alignments-{language}-PanLex.tsv'
file_filter_output = f'../../data/{language}/New_Ids/filtered-tokens-aligned-{language}.tsv'

# Gold Alignment Settings
file_gold_tokens = f'../../data/{language}/New_Ids/tokens-gold-{language}.tsv'
file_output_aligned = f'../../data/{language}/New_Ids/{language}-carried-senses.tsv'

# Add WSD
WSD_system = "AMuSE"
path_WSD = f"../../data/{language}/New_Ids/aligned-tokens-WSD-{language}.tsv"

# Tokens to key files
file_key_output = f'../../data/{language}/New_Ids/silver-key-{language}.txt'

# Evaluate
gold_key_file = f'../../data/{language}/New_Ids/gold-key-{language}.txt'
silver_key_file = f'../../data/{language}/New_Ids/silver-key-{language}.txt'

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
       filter_PanLex, filter_POS)

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

calculate_scores(gold_key_file,
                 silver_key_file)

import pandas as pd
import csv
langauge = "Farsi"
path_gold = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{langauge}/gold-tokens-{langauge}.tsv"
path_WSD = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{langauge}/{langauge}-WSD.tsv"
gold_df = pd.read_csv(path_gold, delimiter='\t', quoting=csv.QUOTE_NONE,encoding="utf-8-sig")
WSD_df = pd.read_csv(path_WSD, delimiter='\t', quoting=csv.QUOTE_NONE, encoding="utf-8-sig")
sentence_ids = []
for x in gold_df["Token ID"]:
    sentence_ids.append(x[0:9])
sentence_ids = set(sentence_ids)
# print(silver_df.head())
output_file = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{langauge}/aligned-tokens-WSD-{langauge}.tsv"

silver_tags = WSD_df[WSD_df["BN Synset"].notnull()]
gold_df["BN Synset"] = None
count = 1
for y in sentence_ids:
    # print(y)
    WSD_sentence = WSD_df[WSD_df['Token ID'].str[:9] == y]
    # print(silver_sentence)
    gold_sentence = gold_df[gold_df['Token ID'].str[:9] == y]
    token_keys = list(gold_sentence["Token"].keys())
    tokens = [x.lower() for x in list(gold_sentence["Token"])]
    # print(gold_df.iloc[tokens[0]]['Token'])
    # print(tokens)
    for x in range(len(WSD_sentence)):
        # print(silver_sentence.iloc[x]["BN Synset"])
            # print(silver_sentence.iloc[x]["Token"])
        if WSD_sentence.iloc[x]["Token"] in tokens:
            a = tokens.index(WSD_sentence.iloc[x]["Token"])
            gold_df.loc[token_keys[a],"BN Synset"] = WSD_sentence.iloc[x]["BN Synset"]



gold_df.to_csv(output_file, sep='\t', index=False,encoding="utf-8-sig")


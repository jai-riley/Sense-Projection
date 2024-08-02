import pandas as pd
import csv

gold_file = "/Users/jairiley/Desktop/Research/Sense-Projection/data/English/Original/gold-sentences-English-2017.tsv"
gold_df = pd.read_csv(gold_file, delimiter='\t', quoting=csv.QUOTE_NONE)

new_file = "/Users/jairiley/Desktop/Research/Sense-Projection/data/all-sentences-aligned.tsv"
new_df = pd.read_csv(new_file, delimiter='\t')

# new_df["Universal ID"] = None
#
# for x in range(len(new_df["English"])):
#     if x % 10 == x:
#         new_df.loc[x,"Universal ID"] = f'd001.s00{x+1}'
#     elif x % 100 == x:
#         new_df.loc[x,"Universal ID"] = f'd001.s0{x+1}'
#     else:
#         new_df.loc[x,"Universal ID"] = f'd001.s{x+1}'

new_df["English ID"] = None
old = 0
new = 0
punct =[ ".", "?", "!"]
old_s = gold_df.iloc[old]["Sentence"]
new_s = new_df.iloc[new]["English"]
id = gold_df.iloc[old]["ID"]
while old < len(gold_df["Sentence"]):

    print(old_s, '\n',new_s,'\n\n')
    if old_s[-1] not in punct:
        old_s += " ."
    if new_s == old_s:
        new_df.loc[new, "English ID"] = id
        old += 1
        new += 1
        if old < len(gold_df["Sentence"]):
            old_s = gold_df.iloc[old]["Sentence"]
            new_s = new_df.iloc[new]["English"]
            id = gold_df.iloc[old]["ID"]
        else:
            break
    else:
        # if old_s < new_s:
        old += 1
        old_s += " "+gold_df.iloc[old]["Sentence"]
        id += ";"+gold_df.iloc[old]["ID"]
        # else:
        #     # print(id)
        #     new += 1
        #     new_s += " "+new_df.iloc[new]["English"]
            # id += ";"+gold_df.iloc[old]["ID"]


new_df.to_csv(new_file, sep='\t', index=False)

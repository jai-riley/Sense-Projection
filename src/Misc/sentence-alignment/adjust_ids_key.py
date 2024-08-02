import pandas as pd
import csv


language = "Italian"
lang_code = 'it'
new_file = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/Original/{language}-aligned-ids.csv"
new_df = pd.read_csv(new_file, delimiter='\t', quoting=csv.QUOTE_NONE)
key_file = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/Original/semeval-2015-task-13-{lang_code}-WSD.tsv"
key_df = pd.read_csv(key_file, delimiter='\t', quoting=csv.QUOTE_NONE, header=None)

d = {}
for x in range(len(new_df['New ID'])):
    d[new_df.loc[x,"Old ID"]] = new_df.loc[x,"New ID"]

# print(d.keys())
for x in range(len(key_df[0])):
    # print(key_df.iloc[x][0])
    # print(key_df.loc[1,x])
    # p
    # print(key_df.loc[x, 0],key_df.loc[x, 1])
    key_df.loc[x, 0] = d[key_df.iloc[x][0]]
    key_df.loc[x, 1] = key_df.iloc[x][1].split(";")[0]

    # key_df.loc[x, 1] = d[key_df.iloc[x][1]]

key_df.to_csv(f'/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/aligned_2017/{language}-new-key.tsv', sep='\t', index=False, header=None)

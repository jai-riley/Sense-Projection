import csv
import pandas as pd
def get_all(path,num = None):

    d = {}
    if num is None:
        df = pd.read_csv(path, delimiter='\t', quoting=csv.QUOTE_NONE)
        for x in range(len(df)):
            if df['Start'].iloc[x] not in d.keys():
                d[df['Start'].iloc[x]] = [df['BN Synset'].iloc[x]]
            else:
                d[df['Start'].iloc[x]].append(df['BN Synset'].iloc[x])
    else:
        df = pd.read_csv(path, delimiter='\t', header=None, quoting=csv.QUOTE_NONE)
        for x in range(len(df)):
            if df[0].iloc[x] not in d.keys():
                d[df[0].iloc[x]] = [df[2].iloc[x]]
            else:
                d[df[0].iloc[x]].append(df[2].iloc[x])
    return d

def read_file(gold_file_path, silver_file_path):
    silver = get_all(silver_file_path)
    gold = get_all(gold_file_path,'yes')
    # print(gold)
    eval(gold,silver)

def eval(gold,silver):
    correct = 0
    incorrect = 0
    for x in silver.keys():
        if x in gold.keys():
            for y in range(len(silver[x])):
                if silver[x][y] in gold[x]:
                    correct += 1
                else:
                    incorrect += 1
        else:
            incorrect += 1
    print(correct/(correct+incorrect))


read_file('../../data/Italian/semeval-2015-task-13-it.tsv','../../data/Italian/Italian-key.tsv')



# Spanish 0.43777777777777777
# Italian 0.37844611528822053

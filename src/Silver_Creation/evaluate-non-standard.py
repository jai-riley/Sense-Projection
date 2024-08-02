import pandas as pd
import csv
from sklearn.metrics import precision_score, recall_score, f1_score

def get_results(path_gold,path_silver):
    gold_df = pd.read_csv(path_gold, delimiter='\t', quoting=csv.QUOTE_NONE)
    silver_df = pd.read_csv(path_silver, delimiter='\t', quoting=csv.QUOTE_NONE)
    gold_df['BN Synset'] = gold_df['BN Synset'].fillna('n/a')
    silver_df['BN Synset'] = silver_df['BN Synset'].fillna('n/a')
    c1 = 0
    c2 = 0
    c3 = 0
    c4 = 0
    c5 = 0
    for x in range(len(gold_df)):
        # gold has no sense
        if gold_df['BN Synset'].iloc[x] == 'n/a':
            # silver has no sense
            if silver_df['BN Synset'].iloc[x] == 'n/a':
                c5 += 1
            # silver has sense
            else:
                c4 += 1
        # gold has sense
        else:
            senses_gold = gold_df['BN Synset'].iloc[x].split(";")
            senses_silver = silver_df['BN Synset'].iloc[x].split(";")
            # silver has no sense
            if silver_df['BN Synset'].iloc[x] == 'n/a':
                c3 += 1
            # silver has same sense
            else:
                for x in senses_silver:
                    if x in senses_gold:
                        c1 += 1
                    else:

                        # silver has different sense
                        c2 += 1

    print(c1,c2,c3,c4,c5)
    # print(f"Accuracy: {(TP)/(FP+TP+FN_1+FN_2)}")
    p = c1/(c1+c2+c4)
    r = c1/(c1+c2+c3)
    c = (c1+c2)/(c1+c2+c3)
    print(f"Precision: {p}")
    print(f"Recall: {r}")
    print(f"F1: {2*((p*r)/(p+r))}")
    print(f"Coverage: {c}")


language = "Spanish"
get_results(f'../../data/{language}/New_Ids/new-gold-tokens-{language}-wSenses.tsv',f'../../data/{language}/New_Ids/{language}-carried-senses.tsv')

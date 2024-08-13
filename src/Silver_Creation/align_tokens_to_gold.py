import pandas as pd
import csv

def create_carried_sheet(path_gold,path_silver,output_file,lan_code):
    gold_df = pd.read_csv(path_gold, delimiter='\t', quoting=csv.QUOTE_NONE)
    silver_df = pd.read_csv(path_silver, delimiter='\t', quoting=csv.QUOTE_NONE)
    silver_df['BN Synset'] = None
    result = gold_df[gold_df['BN Synset'].notnull()]
    # print(result)
    for x in range(len(result['BN Synset'])):
        y = silver_df.loc[silver_df['Token ID'] == result[f'Token ID {lan_code}'].iloc[x]]
        if not y.empty:
            # silver_df.loc[y.index.values[0],"BN Synset"] = result[f'Sense {lan_code}'].iloc[x]
            silver_df.loc[y.index.values[0],"BN Synset"] = result[f'BN Synset'].iloc[x]
    for x in range(len(result[f'POS {lan_code}'])):
        y = silver_df.loc[silver_df['Token ID'] == result[f'Token ID {lan_code}'].iloc[x]]
        if not y.empty:
            # print(silver_df.iloc[y.index.values[0]][f"POS"],result[f'POS {lan_code}'].iloc[x])
            # silver_df.loc[y.index.values[0],"BN Synset"] = result[f'Sense {lan_code}'].iloc[x]
            silver_df.loc[y.index.values[0],f"POS"] = result[f'POS {lan_code}'].iloc[x]
            # print(silver_df.iloc[y.index.values[0]][f"POS"],"\n")

    silver_df.to_csv(output_file, sep='\t', index=False)

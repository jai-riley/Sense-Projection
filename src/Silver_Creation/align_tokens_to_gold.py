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
            silver_df.loc[y.index.values[0],"BN Synset"] = result[f'Sense {lan_code}'].iloc[x]
    silver_df.to_csv(output_file, sep='\t', index=False)

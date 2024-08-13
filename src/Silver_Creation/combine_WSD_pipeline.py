import pandas as pd
import csv

def combine_with_WSD(path_WSD, path_silver):
    WSD_df = pd.read_csv(path_WSD, delimiter='\t', quoting=csv.QUOTE_NONE)
    silver_df = pd.read_csv(path_silver, delimiter='\t', quoting=csv.QUOTE_NONE)
    # silver_df["Add Annotation"] = None
    for x in range(len(WSD_df["Token"])):
        if str(WSD_df.iloc[x]["BN Synset"]) != "nan" and str(silver_df.iloc[x]["BN Synset"]) == "nan":
            silver_df.loc[x,"BN Synset"] = WSD_df.iloc[x]["BN Synset"]
            # silver_df.loc[x,"Add Annotation"] = 1
    silver_df.to_csv(path_silver, sep='\t', index=False)

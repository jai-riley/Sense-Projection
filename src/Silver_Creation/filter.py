import csv
import pandas as pd
# pos_tags = {"NOUN":"n", "VERB":"v","ADJ":"a","ADV":"r"}
pos_tags = {"DET":"x", "NOUN":"n", "VERB":"v","ADJ":"a","ADV":"r", "SCONJ":"x", "PUNCT":"x", "PRON":"x", "CCONJ": "r", "ADP":"x", "NUM":"x"}

def filter(file_aligned, file_BabelNet, file_PanLex, file_output, lang_code,filter_Babel=False, filter_Panlex=False, filter_POS=False):
    df_aligned = pd.read_csv(file_aligned, delimiter='\t', quoting=csv.QUOTE_NONE)
    # df_aligned[f"Sense {lang_code}"] = df_aligned[f"Sense {lang_code}"].fillna('n/a')
    df_aligned["BN Synset"] = df_aligned["BN Synset"].fillna('n/a')

    if filter_Babel:
        df_Babel_errors = pd.read_csv(file_BabelNet, delimiter='\t', quoting=csv.QUOTE_NONE)
        for x in range(len(df_Babel_errors['Row'])):
            if len(df_Babel_errors.iloc[x]['Source']) >= 3 and len(df_Babel_errors.iloc[x]['Target']) >= 3:
                if df_Babel_errors.iloc[x]['Source'][0:3] != df_Babel_errors.iloc[x]['Target'][0:3]:
                    num = df_Babel_errors.iloc[x]['Row']
                    df_aligned.loc[num, "BN Synset"] = 'n/a'
                    # df_aligned.loc[num, f"Sense {lang_code}"] = 'n/a'
    if filter_Panlex:
        count = 0
        df_PanLex_errors = pd.read_csv(file_PanLex, delimiter='\t', quoting=csv.QUOTE_NONE)
        for x in range(len(df_PanLex_errors['Row'])):
            if "#" not in df_PanLex_errors.iloc[x]['Target']:
                # print(df_PanLex_errors.iloc[x]['Target'])
                if len(df_PanLex_errors.iloc[x]['Source']) >= 3 and len(df_PanLex_errors.iloc[x]['Target']) >= 3:
                    if df_PanLex_errors.iloc[x]['Source'][0:3] != df_PanLex_errors.iloc[x]['Target'][0:3]:
                        num = df_PanLex_errors.iloc[x]['Row']
                        # df_aligned.loc[num, f"Sense {lang_code}"] = 'n/a'
                        df_aligned.loc[num, "BN Synset"] = 'n/a'
                        count += 1
            # else:
                # count += 1
        print(count)


    if filter_POS:
        for x in range(len(df_aligned[f'POS {lang_code}'])):
            # senses = df_aligned.iloc[x][f"Sense {lang_code}"].split(';')
            senses = df_aligned.iloc[x][f"BN Synset"].split(';')

            if df_aligned.iloc[x][f'POS {lang_code}'] == "X":
                # df_aligned.loc[x, f"Sense {lang_code}"] = 'n/a'
                df_aligned.loc[x, "BN Synset"] = 'n/a'

            # if df_aligned.iloc[x][f'POS {lang_code}'] is not None and df_aligned.iloc[x][f"Sense {lang_code}"] != 'n/a':
            if df_aligned.iloc[x][f'POS {lang_code}'] is not None and df_aligned.iloc[x][f"BN Synset"] != 'n/a':
                # print(df_aligned.iloc[x][f'POS {lang_code}'])
                if str(df_aligned.iloc[x][f'POS {lang_code}']) != "nan":
                    if "➕" in df_aligned.iloc[x][f'POS {lang_code}']:
                        if "," in df_aligned.iloc[x][f'POS {lang_code}']:
                            pos = df_aligned.iloc[x][f'POS {lang_code}'].split("➕")[1].split(",")[0]
                        else:
                            pos = df_aligned.iloc[x][f'POS {lang_code}'].split("➕")[1]
                    elif "," in df_aligned.iloc[x][f'POS {lang_code}']:
                        pos = df_aligned.iloc[x][f'POS {lang_code}'].split(",")[0]
                    else:
                        pos = df_aligned.iloc[x][f'POS {lang_code}']

                    if pos_tags[pos] != senses[0][-1]:
                        # print(df_aligned.iloc[x][f'POS {lang_code}'], senses[0][-1])

                        # if df_aligned.iloc[x][f'POS {lang_code}'].lower() == 'j':
                        #     if senses[0][-1] != 'a':
                        #         df_aligned.loc[x, f"Sense {lang_code}"] = 'n/a'
                        # else:
                        # df_aligned.loc[x, f"Sense {lang_code}"] = 'n/a'
                        df_aligned.loc[x, f"BN Synset"] = 'n/a'

                # else:
                #     # df_aligned.loc[x, f"Sense {lang_code}"] = 'n/a'
                #     df_aligned.loc[x, "BN Synset"] = 'n/a'

    df_aligned.to_csv(file_output, sep='\t', index=False)




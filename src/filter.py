import csv
import pandas as pd
import re

# pos_tags = {"NOUN":"n", "VERB":"v","ADJ":"a","ADV":"r"}
pos_tags = {"DET": "x", "NOUN": "n", "VERB": "v", "ADJ": "a", "ADV": "r", "SCONJ": "x", "PUNCT": "x", "PRON": "x",
            "CCONJ": "r", "ADP": "x", "NUM": "x", "N": "n", "A": "a", "V": "v", "R": 'r', "X": "x"}


def filter(file_aligned,file_in_Babel, file_VahidN, file_Aryanpour, file_output, file_Babel_Translations,
           file_Panlex_Translations, lang_code, filter_Babel=False, filter_Panlex=False, filter_POS=False,
           filter_VahidN=False, filter_Aryanpour=False):
    df_aligned = pd.read_csv(file_aligned, delimiter='\t', quoting=csv.QUOTE_NONE)
    df_aligned["BN Synset"] = df_aligned["BN Synset"].fillna('n/a')
    df_inBabel = pd.read_csv(file_in_Babel, delimiter="\t", quoting=csv.QUOTE_NONE,header=None)
    values = [filter_Babel, filter_Panlex, filter_VahidN, filter_Aryanpour]
    files = [file_Babel_Translations, file_Panlex_Translations, file_VahidN, file_Aryanpour]
    list_dicts = []
    for x in range(4):
        if values[x]:
            list_dicts.append(pd.read_csv(files[x], delimiter="\t", quoting=csv.QUOTE_NONE, header=None))
    if True in values:
        df_aligned = combine_dict(df_aligned, list_dicts,df_inBabel)

    if filter_POS:
        for x in range(len(df_aligned[f'POS {lang_code}'])):
            # senses = df_aligned.iloc[x][f"Sense {lang_code}"].split(';')
            senses = df_aligned.iloc[x][f"BN Synset"].split(';')

            if df_aligned.iloc[x][f'POS {lang_code}'] == "X":
                # df_aligned.loc[x, f"Sense {lang_code}"] = 'n/a'
                df_aligned.loc[x, "BN Synset"] = 'n/a'

            # if df_aligned.iloc[x][f'POS {lang_code}'] is not None and df_aligned.iloc[x][f"Sense {lang_code}"] != 'n/a':
            if df_aligned.iloc[x][f'POS {lang_code}'] is not None and df_aligned.iloc[x][f"BN Synset"] != 'n/a':
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
                        df_aligned.loc[x, f"BN Synset"] = 'n/a'

    df_aligned.to_csv(file_output, sep='\t', index=False)


def results_dict(df_aligned, df_translations):
    d = []
    for x in range(len(df_translations[4])):
        remove = False
        all_no = False
        if "#" not in df_translations.iloc[x][2] and "➕" not in df_translations.iloc[x][2]:
            if df_translations.iloc[x][4] == 0:
                # remove = True
                if type(df_translations.iloc[x][3]) == str:
                    translations = re.sub(r"[\[\]' ]", "", df_translations.iloc[x][3]).split(",")
                else:
                    translations = df_translations.iloc[x][3]
                all_no = False
                if len(translations) >= 1:
                    # remove = True
                    for word in translations:
                        if len(word) >= 3:
                            if df_translations.iloc[x][2] in word:
                                all_no = True
                            if word in df_translations.iloc[x][2]:
                                all_no = True
                    if df_translations.iloc[x][1][:3] != df_translations.iloc[x][2][:3]:
                        remove = True
                    else:
                        print(df_translations.iloc[x][1], df_translations.iloc[x][2])
        if remove or all_no:
            num = df_translations.iloc[x][0]
            df_aligned.loc[num, "BN Synset"] = 'n/a'
    return df_aligned


def combine_dict(df_aligned, list_of_dicts,in_babel):
    df = pd.DataFrame(columns=["Row", "Source", "Target", "Translations", "Valid?"])
    count = 0
    for di in list_of_dicts:
        for x in range(len(di[3])):
            translations = re.sub(r"[\[\]' ]", "", di.iloc[x][3]).split(",")
            if di.iloc[x][0] not in list(df["Row"]):
                if len(translations) == 1 and translations[0] == '':
                    df.loc[count] = [di.iloc[x][0], di.iloc[x][1], di.iloc[x][2], [], 1]
                else:
                    df.loc[count] = [di.iloc[x][0], di.iloc[x][1], di.iloc[x][2], translations, di.iloc[x][4]]
                count += 1
            else:
                idx = list(df["Row"]).index(di.iloc[x][0])
                for trans in translations:
                    if trans != '':
                        df.loc[idx, "Translations"].append(trans)
                if len(translations) == 1 and translations[0] == '':
                    df.loc[idx, "Valid?"] = 1
                if di.iloc[x][4] == 1:
                    df.loc[idx, "Valid?"] = 1

    for x in range(len(in_babel[2])):
        idx = list(df["Row"]).index(in_babel.iloc[x][0])
        if in_babel.iloc[x][2] == 0:
            df.loc[idx, "Valid?"] = 1


    df.columns = [0, 1, 2, 3, 4]
    return results_dict(df_aligned, df)

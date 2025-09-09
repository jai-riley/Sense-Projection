import csv
import pandas as pd
import re

pos_tags = {
    "DET": "x", "NOUN": "n", "VERB": "v", "ADJ": "a", "ADV": "r",
    "SCONJ": "x", "PUNCT": "x", "PRON": "x", "CCONJ": "r", "ADP": "x",
    "NUM": "x", "N": "n", "A": "a", "V": "v", "R": "r", "X": "x"
}


def filter(file_aligned, files, filters, lang_code, filter_POS=False, file_output=None):
    """
    Filter aligned word sense data based on dictionary lookups and POS constraints.

    Parameters
    ----------
    file_aligned : str
        Path to the aligned file containing the base data (tab-separated).
    files : list of str
        List of translation-related files in the following order:
        [inBabel, Babel_Translations, Panlex_Translations, VahidN, Aryanpour].
    filters : list of bool
        List of flags (same length as `files`) indicating which translation
        dictionaries should be used. The first entry (inBabel) is always loaded
        regardless of its flag.
    lang_code : str
        Language code (e.g., "en") corresponding to the POS column in the aligned file.
    filter_POS : bool, optional
        Whether to filter synsets by POS agreement. Default is False.
    file_output : str, optional
        Path to save the filtered DataFrame as a tab-separated file. If None,
        no file is saved.

    Returns
    -------
    pandas.DataFrame
        The filtered aligned DataFrame.
    """
    df_aligned = pd.read_csv(file_aligned, delimiter='\t', quoting=csv.QUOTE_NONE)
    df_aligned["BN Synset"] = df_aligned["BN Synset"].fillna('n/a')

    # Always load "in Babel" file (assumed first in list)
    df_inBabel = pd.read_csv(files[0], delimiter="\t", quoting=csv.QUOTE_NONE, header=None)

    # Collect only the active dictionaries
    list_dicts = []
    for file, use in zip(files[1:], filters[1:]):  # skip inBabel (index 0)
        if use:
            list_dicts.append(pd.read_csv(file, delimiter="\t", quoting=csv.QUOTE_NONE, header=None))

    # If any dictionaries used, combine
    if any(filters[1:]):
        df_aligned = combine_dict(df_aligned, list_dicts, df_inBabel)

    # POS filtering
    if filter_POS:
        for x in range(len(df_aligned[f'POS {lang_code}'])):
            senses = df_aligned.iloc[x]["BN Synset"].split(';')

            if df_aligned.iloc[x][f'POS {lang_code}'] == "X":
                df_aligned.loc[x, "BN Synset"] = 'n/a'

            if (
                df_aligned.iloc[x][f'POS {lang_code}'] is not None
                and df_aligned.iloc[x]["BN Synset"] != 'n/a'
            ):
                if str(df_aligned.iloc[x][f'POS {lang_code}']) != "nan":
                    pos_str = str(df_aligned.iloc[x][f'POS {lang_code}'])
                    if "➕" in pos_str:
                        if "," in pos_str:
                            pos = pos_str.split("➕")[1].split(",")[0]
                        else:
                            pos = pos_str.split("➕")[1]
                    elif "," in pos_str:
                        pos = pos_str.split(",")[0]
                    else:
                        pos = pos_str

                    if pos_tags.get(pos, "x") != senses[0][-1]:
                        df_aligned.loc[x, "BN Synset"] = 'n/a'

    if file_output:
        df_aligned.to_csv(file_output, sep='\t', index=False)

    return df_aligned


def results_dict(df_aligned, df_translations):
    """
    Apply translation-based filtering to the aligned DataFrame.

    Parameters
    ----------
    df_aligned : pandas.DataFrame
        The aligned word sense DataFrame.
    df_translations : pandas.DataFrame
        Translation dictionary entries with columns:
        [Row, Source, Target, Translations, Valid?].

    Returns
    -------
    pandas.DataFrame
        Updated `df_aligned` with invalid entries marked as 'n/a' in BN Synset.
    """
    for x in range(len(df_translations[4])):
        remove = False
        all_no = False
        if "#" not in df_translations.iloc[x][2] and "➕" not in df_translations.iloc[x][2]:
            if df_translations.iloc[x][4] == 0:
                if isinstance(df_translations.iloc[x][3], str):
                    translations = re.sub(r"[\[\]' ]", "", df_translations.iloc[x][3]).split(",")
                else:
                    translations = df_translations.iloc[x][3]
                if translations:
                    for word in translations:
                        if len(word) >= 3:
                            if df_translations.iloc[x][2] in word or word in df_translations.iloc[x][2]:
                                all_no = True
                    if df_translations.iloc[x][1][:3] != df_translations.iloc[x][2][:3]:
                        remove = True
                    else:
                        print(df_translations.iloc[x][1], df_translations.iloc[x][2])
        if remove or all_no:
            num = df_translations.iloc[x][0]
            df_aligned.loc[num, "BN Synset"] = 'n/a'
    return df_aligned


def combine_dict(df_aligned, list_of_dicts, in_babel):
    """
    Combine multiple translation dictionaries into a unified DataFrame
    and apply translation-based filtering.

    Parameters
    ----------
    df_aligned : pandas.DataFrame
        The aligned word sense DataFrame.
    list_of_dicts : list of pandas.DataFrame
        A list of translation dictionary DataFrames to merge.
    in_babel : pandas.DataFrame
        The "in Babel" DataFrame used to adjust validity flags.

    Returns
    -------
    pandas.DataFrame
        Updated `df_aligned` with translations merged and filtered.
    """
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
                    if trans:
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


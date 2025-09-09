import subprocess
import json
import csv
import pandas as pd


def read_tsv_column_to_list(file_path, column_name, other_column):
    """
    Reads values from a specified column in a TSV file. If the value is empty,
    uses an alternative column instead.

    Parameters
    ----------
    file_path : str
        Path to the TSV file.
    column_name : str
        Name of the primary column to read from.
    other_column : str
        Name of the fallback column to use if the primary column value is empty.

    Returns
    -------
    list
        A list of values from the specified column, with fallbacks applied.
    """
    items = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                if column_name in row:
                    if str(row[column_name]) == "":
                        items.append(row[other_column])
                    else:
                        items.append(row[column_name])
                else:
                    print(f"Column '{column_name}' not found in the file.")
                    return []
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    return items


def run_panlex(source_word, target_word, uid_value="eng-000", target_uid="zho-000"):
    """
    Queries the PanLex API for translations of a source word.

    Parameters
    ----------
    source_word : str
        The word in the source language (must match `uid_value`).
    target_word : str
        The corresponding target word (used for validation).
    uid_value : str, optional
        PanLex UID for the source language (default "eng-000").
    target_uid : str, optional
        PanLex UID for the target language (default "zho-000").

    Returns
    -------
    list of dict
        A list of translation results from PanLex API. Each dict contains
        keys like 'id', 'txt', and 'txt_degr'.

    Notes
    -----
    - Calls `curl` through subprocess (not the most efficient — could be replaced
      with `requests` for cleaner code).
    - Currently hardcoded to English ("eng-000") → Chinese ("zho-000").
    """
    results = []
    if source_word != "":
        try:
            if target_word != "":
                print(source_word, target_word)

                # First query: get expression ID for source word
                result = subprocess.run(
                    f'curl http://api.panlex.org/v2/expr -d \'{{ "uid": "{uid_value}", "txt": "{source_word}" }}\'',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                response_json = json.loads(result.stdout)
                results = response_json['result']
                trans_expr_value = results[0]['id']
                print(trans_expr_value)

                # Second query: translate to target language
                result = subprocess.run(
                    f'curl http://api.panlex.org/v2/expr -d \'{{ "uid": "{target_uid}", "trans_expr": {trans_expr_value} }}\'',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                response_json = json.loads(result.stdout)
                results = response_json["result"]
                print(results)

        except Exception as e:
            print(e)
            if str(e) != "list index out of range" and source_word != '""""' and source_word.isalpha():
                return run_panlex(source_word, target_word, uid_value, target_uid)
    return results

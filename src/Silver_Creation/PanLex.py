import subprocess
import json
import csv
import pandas as pd
def read_tsv_column_to_list(file_path, column_name,other_column):
    """
    Reads a specified column from a TSV file and adds all items to a list.

    :param file_path: Path to the TSV file
    :param column_name: Name of the column to read from
    :return: List containing all items from the specified column
    """
    items = []

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                if column_name in row:
                    if row[column_name] is None:
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

file_path = '/Users/jairiley/Desktop/Research/Sense-Projection/data/Spanish/aligned_2017/tokens-aligned-Spanish.tsv'
column_name = 'Token ES'
silver = read_tsv_column_to_list(file_path, "Lemma ES", column_name)
column_name = 'Token'
gold = read_tsv_column_to_list(file_path, 'Lemma',column_name)
print(len(silver),len(gold))

correct = 0
total = 0
incorrect = 0
l = []
for x in range(len(gold)):
    print(f"{x} of {len(gold)}")
    uid_value = "eng-000"
    txt_value = gold[x].lower()
    if txt_value != "":
        try:
            if silver[x] != "":
                result = subprocess.run(
                    f'curl http://api.panlex.org/v2/expr -d \'{{ "uid": "{uid_value}", "txt": "{txt_value}" }}\'',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                # print(result)
                # Parse the JSON response
                response_json = json.loads(result.stdout)
                # print(response_json)
                # Access the 'result' list
                results = response_json['result']
                # print(results)
                # Print the results
                # results[0]['id']
                trans_expr_value = results[0]['id']

                # Run the curl command and capture the output
                result = subprocess.run(
                    f'curl http://api.panlex.org/v2/expr -d \'{{ "uid": "spa-000", "trans_expr": {trans_expr_value} }}\'',
                    shell=True,
                    capture_output=True,
                    text=True
                )

                # Parse the JSON response
                response_json = json.loads(result.stdout)

                # Access the 'result' list
                results = response_json['result']

                # Print the results
                list_of_translations = []
                for item in results:
                    list_of_translations.append(item['txt'])
                if silver[x].lower() in list_of_translations or silver[x].lower() == txt_value:
                    correct += 1
                else:
                    incorrect += 1
                    l.append([x,gold[x],silver[x]])
                total += 1
        except:

            if silver[x].lower() == gold[x].lower():
                correct += 1
                total += 1
            # else:
            #     print("yes")
            #     incorrect += 1
            #     l.append([x,gold[x],silver[x]])

print(correct/total)

df = pd.DataFrame(l, columns=['Row', 'Source','Target'])
df.to_csv('../../data/Spanish/aligned_2017/problem-alignments-Spanish-PanLex.tsv', sep='\t', index=False)

# Italian 85.5
# Spanish 85.9

# New Spanish
# 0.8503046127067014

# New Italian
# 0.8485663082437276

# 2017 Italian
# 0.8216123499142367

# 2017 Spanish
# 0.8221070811744386

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

def run_panlex(source_word,target_word):
    uid_value = "eng-000"
    results = []
    if source_word != "":
        try:
            if target_word != "":
                print(source_word, target_word)
                result = subprocess.run(
                    f'curl http://api.panlex.org/v2/expr -d \'{{ "uid": "{uid_value}", "txt": "{source_word}" }}\'',
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
                trans_expr_value = results[0]['id']
                print(trans_expr_value)

                # Run the curl command and capture the output
                result = subprocess.run(
                    f'curl http://api.panlex.org/v2/expr -d \'{{ "uid": "zho-000", "trans_expr": {trans_expr_value} }}\'',
                    shell=True,
                    capture_output=True,
                    text=True
                )

                # Parse the JSON response
                response_json = json.loads(result.stdout)

                # Access the 'result' list
                results = response_json["result"]
                print(results)


        except Exception as e:
            print(e)
            if str(e) != "list index out of range" and source_word != '""""' and source_word.isalpha():
                return run_panlex(source_word,target_word)

            # return []
            # if silver[x].lower() == gold[x].lower():
            #     correct += 1
            #     total += 1
            #     writer.writerow(
            #         {"Source": gold[x], "Target": silver[x], "Translations": "not in panlex", "Valid?": 1})
            # else:
            #     writer.writerow(
            #         {"Source": gold[x], "Target": silver[x], "Translations": "not in panlex", "Valid?": 0})
    return results

file_path = '/Sense-Projection/data/Chinese/second/tokens-aligned-Chinese.tsv'
column_name = 'Token ZH'
silver = read_tsv_column_to_list(file_path, "Token ZH", column_name)
column_name = 'Token'
gold = read_tsv_column_to_list(file_path, 'Lemma',column_name)
print(len(silver),len(gold))

correct = 0
total = 0
incorrect = 0
l = []
file_path = '/Users/jairiley/Desktop/Research/Sense-Projection/data/Chinese/PanLex-Translations-Chinese.tsv'
with open(file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, delimiter='\t',fieldnames=["Row","Source","Target","Translations","Valid?"])
    for x in range(len(gold)):
        print(f"{x} of {len(gold)}")
        source_word = gold[x].lower()
        target_word = silver[x].lower()
        if source_word != "" and target_word != "":
            results = run_panlex(source_word,target_word)

            # print(results)
            # Print the results
            list_of_translations = []
            for item in results:
                # print(item['txt'])
                list_of_translations.append(item['txt'])
                if item['txt'] != item['txt_degr']:
                    list_of_translations.append(item['txt_degr'])
            if "#" in silver[x] or "➕" in silver[x]:
                if "#" in silver[x]:
                    target_word = silver[x].split("#")
                else:
                    target_word = silver[x].split("➕")
                    is_in = False
                    a = ";".join(list_of_translations)
                    for word in target_word:
                        if word in a or word in source_word or source_word in word:
                        # if word in list_of_translations:
                            is_in = True
                        else:
                            for w in list_of_translations:
                                if w in word:
                                    is_in = True
                    if is_in:
                        correct += 1
                        print('in')
                        writer.writerow(
                            {"Row":x,"Source": source_word, "Target": target_word, "Translations": list_of_translations,
                             "Valid?": 1})
                    else:
                        print("out")
                        incorrect += 1
                        # print(gold[x], target_word)
                        l.append([x, gold[x], silver[x]])
                        writer.writerow(
                            {"Row":x,"Source": source_word, "Target": target_word, "Translations": list_of_translations,
                             "Valid?": 0})

            else:
                target_word = silver[x].lower()
                a = ";".join(list_of_translations)
                if target_word in a or target_word in source_word or source_word in target_word:
                # if target_word in list_of_translations:
                    correct += 1
                    print("in")
                    writer.writerow(
                        {"Row":x,"Source": source_word, "Target": target_word, "Translations": list_of_translations,
                         "Valid?": 1})
                else:
                    is_in = False
                    for w in list_of_translations:
                        if w in target_word:
                            is_in = True
                    if is_in:
                        correct += 1
                        print("in")
                        writer.writerow(
                            {"Row":x,"Source": source_word, "Target": target_word, "Translations": list_of_translations,
                             "Valid?": 1})
                    else:
                        print("out")
                        incorrect += 1
                        # print(gold[x], target_word)
                        l.append([x, gold[x], silver[x]])
                        writer.writerow(
                            {"Row":x,"Source": source_word, "Target": target_word, "Translations": list_of_translations,
                             "Valid?": 0})

            total += 1

        # else:
        #     print("yes")
        #     incorrect += 1
        #     l.append([x,gold[x],silver[x]])

print(correct/total)

df = pd.DataFrame(l, columns=['Row', 'Source','Target'])
df.to_csv('/Users/jairiley/Desktop/Research/Sense-Projection/data/Chinese/second/problem-alignments-Chinese-Panlex.tsv', sep='\t', index=False)

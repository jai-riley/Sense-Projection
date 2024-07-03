import csv
from get_wsd import get_wsd

def find_multi_lexical_in_alignment(document_number: int, sentence_number: int, token: str) -> bool:
    for value in multi_lexical:
        document_id = int(value[0].split('.')[0][1:])
        sentence_id = int(value[0].split('.')[1][1:])
        if document_id == document_number and sentence_number == sentence_id and token == value[2]:
            return True

    return False





multi_lexical = []


key_file = []
with open("a3_tokens-FAMerge.csv", 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)

    next(reader)

    for row in reader:
        if row[6] != '':
            key_file.append([row[0],row[0],row[6], ""])
            document_number = int(row[0].split('.')[0][1:])
            sentence_number = int(row[0].split('.')[1][1:])
            token_number = int(row[0].split('.')[2][1:])

with open('farsi.key', mode='w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(key_file)

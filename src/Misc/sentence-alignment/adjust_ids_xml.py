import pandas as pd
import xml.etree.ElementTree as ET
import csv

new_file = "/Users/jairiley/Desktop/Research/Sense-Projection/data/all-sentences-aligned.tsv"
new_df = pd.read_csv(new_file, delimiter='\t', quoting=csv.QUOTE_NONE)

language = "Italian"
xml_file = f'../../data/{language}/Original/semeval-2015-task-13-it.xml'

# Parse the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Create a list to hold the extracted data
data = []

# Iterate through the XML structure and extract relevant information
for text in root.findall('text'):
    for sentence in text.findall('sentence'):
        for wf in sentence.findall('wf'):
            token_id = wf.get('id')
            lemma = wf.get('lemma', '')
            pos = wf.get('pos', '')
            token = wf.text
            data.append([token_id, token, lemma, pos])

d = {}
for x in range(len(new_df['Universal ID'])):
    print(new_df.iloc[x][f'{language} ID'])
    ids = new_df.iloc[x][f'{language} ID'].split(';')
    for a in ids:
        d[a] = new_df.iloc[x]['Universal ID']
# print(d)
# print(d)
token_count = 0
new_id = ""
sentence_num = ""
token_id = ""

for x in range(len(data)):
    # print(data[x])
    if data[x][0] != None:
        data[x].append(data[x][0])
        # print(data)
        if new_id != d[data[x][0][0:9]]:
            new_id = d[data[x][0][0:9]]
            # print(new_id)
            data[x][0] = f"{new_id}.t001"
            token_count = 1
        elif new_id == d[data[x][0][0:9]]:
            token_count += 1
            if token_count % 10 == token_count:
                token_id = f"t00{token_count}"
            elif token_count % 100 == token_count:
                token_id = f"t0{token_count}"
            else:
                token_id = f"t{token_count}"
            data[x][0] = f"{new_id}.{token_id}"

df = pd.DataFrame(data, columns=['New ID','Token', "Lemma", "POS",'Old ID'])
df.to_csv(f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/Original/{language}-aligned-ids.csv",sep='\t',index=False)

from xml.dom import minidom
import csv


def get_column(csv_file_path, target_column):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter='\t')
        return [row[target_column] for row in csvreader]


def get_num_doc(csv_file_path):
    # print(get_column(csv_file_path, "New ID")[-1])
    return int(get_column(csv_file_path, "New ID")[-1][1:4])


def get_num_sentences(csv_file_path, doc_num):
    column_values = get_column(csv_file_path, "New ID")
    doc = [x for x in column_values if x[0:4] == doc_num]
    return int(doc[-1][6:9])


def add_tokens(sentence_id, input_file, object, root):
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile,delimiter="\t")
        for row in csvreader:
            # print(row)
            if row["New ID"][0:9] == sentence_id:
                token = root.createElement("wf")
                token.setAttribute("id", row["New ID"])
                token.setAttribute("lemma", row["Lemma"])
                token.setAttribute("pos", row["POS"])
                x = root.createTextNode(row["Token"])
                token.appendChild(x)
                object.appendChild(token)


def GenerateXML(input_file, output_file, lang):
    root = minidom.Document()
    xml = root.createElement("corpus")
    xml.setAttribute('lang', lang)
    root.appendChild(xml)
    # print(get_num_doc(input_file) + 1)
    for x in range(1, get_num_doc(input_file) + 1):
        docId = ""
        if x % 10 == x:
            docId = f"d00{x}"
        # add more here if we want to be general
        document = root.createElement('text')
        document.setAttribute('id', docId)
        xml.appendChild(document)
        num_sen = get_num_sentences(input_file, docId)
        # print( num_sen + 1)
        for y in range(1, num_sen + 1):
            if y % 10 == y:
                senId = f"s00{y}"
            elif y % 100 == y:
                senId = f"s0{y}"
            else:
                senId = f"s{y}"
            sentence = root.createElement("sentence")
            sentence.setAttribute('id', f"{docId}.{senId}")
            document.appendChild(sentence)
            add_tokens(f"{docId}.{senId}", input_file, sentence, root)
    xml_str = root.toprettyxml(indent="\t")
    with open(output_file, "w") as f:
        f.write(xml_str)


lang = "IT"
input_file = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/Original/{language}-aligned-ids.csv"
output_file = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/Original/{language}.xml"
GenerateXML(input_file, output_file, lang)

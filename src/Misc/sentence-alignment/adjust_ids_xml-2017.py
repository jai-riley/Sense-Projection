import pandas as pd
import xml.etree.ElementTree as ET
import csv

new_file = "/Users/jairiley/Desktop/Research/Sense-Projection/data/all-sentences-aligned.tsv"
new_df = pd.read_csv(new_file, delimiter='\t', quoting=csv.QUOTE_NONE)

language = "English"
xml_file = f'../../data/{language}/Original/semeval2015_updated.data.xml'

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
    # print(new_df.iloc[x][f'{language} ID'])
    ids = new_df.iloc[x][f'{language} ID'].split(';')
    for a in ids:
        d[a] = new_df.iloc[x]['Universal ID']

# # print(d)
# # print(d)
# token_count = 0
# new_id = ""
# sentence_num = ""
# token_id = ""
#
# for x in range(len(data)):
#     # print(data[x])
#     if data[x][0] != None:
#         data[x].append(data[x][0])
#         # print(data)
#         if new_id != d[data[x][0][0:9]]:
#             new_id = d[data[x][0][0:9]]
#             # print(new_id)
#             data[x][0] = f"{new_id}.t001"
#             token_count = 1
#         elif new_id == d[data[x][0][0:9]]:
#             token_count += 1
#             if token_count % 10 == token_count:
#                 token_id = f"t00{token_count}"
#             elif token_count % 100 == token_count:
#                 token_id = f"t0{token_count}"
#             else:
#                 token_id = f"t{token_count}"
#             data[x][0] = f"{new_id}.{token_id}"
#
# df = pd.DataFrame(data, columns=['New ID','Token', "Lemma", "POS",'Old ID'])
# # df.to_csv(f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/Original/{language}-aligned-ids.csv",sep='\t',index=False)
#
# d = {}
# for x in range(len(df['New ID'])):
#     if df.iloc[x]["Old ID"]:
#         # print(df.iloc[x]["Old ID"])
#         d[df.iloc[x]["Old ID"]] = df.iloc[x]["New ID"]

import xml.etree.ElementTree as ET

# Load the XML file
input_file = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/Original/English.xml"

tree = ET.parse(input_file)
root = tree.getroot()

# Dictionary with updated values

# Iterate through the XML structure and update the non-empty wf elements
for sentence in root.findall(".//text"):
    for wf in sentence.findall("sentence"):
        wf_id = wf.get("id")
        if wf_id and wf_id in d.keys():
            wf.set("id", d[wf_id])



# Write the modified XML back to a file


lang = "EN"
output_file = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/Original/{language}.xml"

tree.write(output_file, encoding='UTF-8', xml_declaration=True)

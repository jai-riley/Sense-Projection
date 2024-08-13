from xml.dom import minidom
import csv
import xml.etree.ElementTree as ET
import re
import pandas
# pos_tags = {"X":"X", "R":"ADV","V":"VERB","N":"NOUN","J":"ADJ"}
pos_tags = {"DET":"X", "NOUN":"NOUN", "VERB":"VERB","ADJ":"ADJ","ADV":"ADV", "SCONJ":"X", "PUNCT":"X", "PRON":"X", "CCONJ": "ADV", "ADP":"X", "NUM":"X", "NOUN,EZ":"NOUN","ADJ,EZ":"ADJ","VERB,EZ":"VERB","ADV,EZ":"ADV"}
def get_column(csv_file_path,target_column):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile,delimiter="\t")
        return [row[target_column] for row in csvreader]

def get_num_doc(csv_file_path):
        return int(get_column(csv_file_path,"Token ID")[-1][1:4])

def get_num_sentences(csv_file_path, doc_num):
    column_values = get_column(csv_file_path,"Token ID")
    doc = [x for x in column_values if x[0:4] == doc_num]
    return int(doc[-1][6:9])

def add_tokens(sentence_id, input_file, object, root):
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile,delimiter="\t")
        token_num = 0
        for row in csvreader:
            if row["Token ID"][0:9] == sentence_id:
                if str(row["BN Synset"]) == "":
                    token = root.createElement("wf")
                    if row["Lemma"] != "":
                        token.setAttribute("lemma", row["Lemma"])
                    pos = pos_tags[row["POS"]]
                    token.setAttribute("pos", pos)
                    x = root.createTextNode(row["Token"])
                    token.appendChild(x)
                    object.appendChild(token)
                else:
                    token = root.createElement("instance")
                    if token_num % 10 == token_num and token_num != 10:
                        token.setAttribute("id",f"{row['Token ID'][0:9]}.t00{token_num}")
                    else:
                        token.setAttribute("id",f"{row['Token ID'][0:9]}.t0{token_num}")
                    token_num += 1
                    token.setAttribute("lemma", row["Lemma"])
                    pos = pos_tags[row["POS"]]
                    token.setAttribute("pos", pos)
                    x = root.createTextNode(row["Token"])
                    token.appendChild(x)
                    object.appendChild(token)


def GenerateXML(input_file,output_file,lang):
    root = minidom.Document()
    xml = root.createElement("corpus")
    xml.setAttribute('lang', lang)
    root.appendChild(xml)
    for x in range(1,get_num_doc(input_file)+1):
        docId = "d001"
        #add more here if we want to be general
        document = root.createElement('text')
        document.setAttribute('id', docId)
        xml.appendChild(document)
        num_sen = get_num_sentences(input_file,docId)
        for y in range(1,num_sen+1):
            if y % 10 == y:
                senId = f"s00{y}"
            elif y % 100 == y:
                senId = f"s0{y}"
            else:
                senId = f"s{y}"

            sentence = root.createElement("sentence")
            sentence.setAttribute('id',f"{docId}.{senId}")
            sentence.setAttribute('source', "semeval2015-en")
            document.appendChild(sentence)
            add_tokens(f"d001.{senId}", input_file, sentence, root)
    xml_str = root.toprettyxml(indent="\t")
    with open(output_file, "w") as f:
        f.write(xml_str)

def fix_key_ids(input_key,output_key):
    with open(input_key, 'r',  encoding='utf-8') as infile, \
        open(output_key, 'w',  encoding='utf-8') as outfile:

        reader = csv.reader(infile, delimiter=' ')
        writer = csv.writer(outfile, delimiter=' ')
        token_num = 0
        sent_num = 0
        current_sent = "d001.s001"
        current_token = "d001.s001.t001"
        for row in reader:
            # print(row[0])
            print(row[0],row[1])
            # if current_token == "d001.s001.t001":
            if current_token != row[0] and current_token != "d001.s001.t001":
                writer.writerow(d)
                token_num += 1
            if row[0][0:9] != current_sent:
                current_sent = row[0][0:9]
                current_token = row[0]
                token_num = 0
                sent_num = int(row[0][6:9])-1
            if token_num % 10 == token_num and token_num != 10:
                tok = f"t00{token_num}"
            else:
                tok = f"t0{token_num}"
            if sent_num % 10 == sent_num and sent_num != 10:
                sent = f"s00{sent_num}"
            elif sent_num % 100 == sent_num and sent_num != 100:
                sent = f"s0{sent_num}"
            else:
                sent = f"s{sent_num}"

            token_id = f"d000.{sent}.{tok}"
            bn_synset = row[1:]

            d = [token_id]
            for a in bn_synset:
                d.append(a)
            # for x in range(len(bn_synset)):
            #     d[f"Sense {x}"] = bn_synset[x]

            current_token = row[0]
            # sent_num+=1

def decrement_sentence_ids(input_file, output_file):
    # Parse the XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Regex pattern to match the id format and capture the parts
    pattern = re.compile(r"(d\d{2,})\.(s\d{3})\.(t\d{3})")
    sentence_pattern = re.compile(r"(d\d{2,})\.(s\d{3})")

    # Iterate through all elements with an 'id' attribute
    for elem in root.findall(".//*[@id]"):
        original_id = elem.get('id')

        # Handle token-level IDs (e.g., d00a.s00b.t00c)
        match = pattern.match(original_id)
        if match:
            doc_part, sentence_part, token_part = match.groups()
            # Decrement the sentence number by 1
            sentence_num = int(sentence_part[1:])
            new_sentence_num = sentence_num - 1
            new_sentence_part = f"s{new_sentence_num:03d}"

            # Form the new id and update the element
            new_id = f"{doc_part}.{new_sentence_part}.{token_part}"
            elem.set('id', new_id)

        # Handle sentence-level IDs (e.g., d00a.s00b)
        match_sentence = sentence_pattern.match(original_id)
        if match_sentence and not pattern.match(original_id):
            doc_part, sentence_part = match_sentence.groups()
            # Decrement the sentence number by 1
            sentence_num = int(sentence_part[1:])
            new_sentence_num = sentence_num - 1
            new_sentence_part = f"s{new_sentence_num:03d}"

            # Form the new id and update the element
            new_id = f"{doc_part}.{new_sentence_part}"
            elem.set('id', new_id)

    # Write the modified XML to the output file
    tree.write(output_file, encoding='utf-8', xml_declaration=True)


lang = "FAR"
langauge = "Farsi"
input_xml = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{langauge}/gold-tokens-{langauge}-wSenses.tsv"
output_xml = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{langauge}/xl-wsd-format-{langauge}.xml"
input_key = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{langauge}/gold-key-{langauge}.txt"
output_key = f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{langauge}/xl-wsd-key-{langauge}.txt"
GenerateXML(input_xml, output_xml, lang)
fix_key_ids(input_key,output_key)


decrement_sentence_ids(output_xml, output_xml)


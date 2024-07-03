from xml.dom import minidom
import csv

def get_column(csv_file_path,target_column):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        return [row[target_column] for row in csvreader]

def get_num_doc(csv_file_path):
        return int(get_column(csv_file_path,"Token ID FAR")[-1][1:4])

def get_num_sentences(csv_file_path, doc_num):
    column_values = get_column(csv_file_path,"Token ID FAR")
    doc = [x for x in column_values if x[0:4] == doc_num]
    return int(doc[-1][6:9])

def add_tokens(sentence_id, input_file, object, root):
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            if row["Token ID FAR"][0:9] == sentence_id:
                token = root.createElement("wf")
                token.setAttribute("id",row["Token ID FAR"])
                token.setAttribute("lemma", row["Farsi Lemma"])
                token.setAttribute("pos", row["POS FAR"])
                x = root.createTextNode(row["Farsi Token"])
                token.appendChild(x)
                object.appendChild(token)

def GenerateXML(input_file,output_file,lang):
    root = minidom.Document()
    xml = root.createElement("corpus")
    xml.setAttribute('lang', lang)
    root.appendChild(xml)
    for x in range(1,get_num_doc(input_file)+1):
        docId = ""
        if x % 10 == x:
            docId = f"f00{x}"
        #add more here if we want to be general
        document = root.createElement('text')
        document.setAttribute('id', docId)
        xml.appendChild(document)
        num_sen = get_num_sentences(input_file,docId)
        for y in range(1,num_sen+1):
            if y % 10 == y:
                senId = f"s00{y}"
            else:
                senId = f"s0{y}"
            sentence = root.createElement("sentence")
            sentence.setAttribute('id',f"{docId}.{senId}")
            document.appendChild(sentence)
            add_tokens(f"{docId}.{senId}", input_file, sentence, root)
    xml_str = root.toprettyxml(indent="\t")
    with open(output_file, "w") as f:
        f.write(xml_str)


if __name__ == "__main__":
    lang = "FA"
    input_file = "a3_tokens-FAMerge.csv"
    output_file = "farsi.xml"
    GenerateXML(input_file,output_file,lang)

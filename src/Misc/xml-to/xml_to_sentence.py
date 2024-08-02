import xml.etree.ElementTree as ET

language = "English"
# Define the input and output file paths
input_file = f'../../data/{language}/2017/{language}.xml'
output_file = f'../../data/{language}/2017/gold-sentences-{language}.tsv'

# Parse the XML file
tree = ET.parse(input_file)
root = tree.getroot()

# Open the output TSV file
with open(output_file, 'w', encoding='utf-8') as tsv_file:
    # Iterate through each sentence in the XML
    tsv_file.write("ID\tSentence\n")
    for text in root.findall('text'):
        for sentence in text.findall('sentence'):
            sentence_id = sentence.get('id')
            sentence_text = ' '.join([word.text for word in sentence.findall('wf')])
            tsv_file.write(f"{sentence_id}\t{sentence_text}\n")

print(f"TSV file has been created at: {output_file}")

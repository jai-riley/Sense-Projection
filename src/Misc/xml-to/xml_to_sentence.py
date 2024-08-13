import xml.etree.ElementTree as ET
import pandas as pd
language = "Italian"
# Define the input and output file paths
input_file = f'/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/new_format/xl-wsd-format-{language}.xml'
output_file = f'/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/new_format/gold-sentences-{language}.tsv'

# Parse the XML file
tree = ET.parse(input_file)
root = tree.getroot()

df = []
# Open the output TSV file
with open(output_file, 'w', encoding='utf-8') as tsv_file:
    # Iterate through each sentence in the XML
    # tsv_file.write("ID\tSentence\n")
    for text in root.findall('text'):
        for sentence in text.findall('sentence'):
            df.append({"ID":sentence.get('id'),"Sentence":' '.join([word.text for word in sentence])})
            # sentence_id = sentence.get('id')
            # sentence_text = ' '.join([word.text for word in sentence])
            # tsv_file.write(f"{sentence_id}\t{sentence_text}\n")
df = pd.DataFrame(df)

df.to_csv(output_file, sep='\t', index=False)
print(f"TSV file has been created at: {output_file}")

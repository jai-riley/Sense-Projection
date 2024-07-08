import pandas as pd
import xml.etree.ElementTree as ET

# File paths
xml_file = '../../data/Spanish/semeval-2015-task-13-es.xml'
tsv_output_file = '../../data/Spanish/tokens_gold_Spanish.tsv'

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

# Create a DataFrame and write it to a TSV file
df = pd.DataFrame(data, columns=['Token ID', 'Token', 'Lemma', 'POS'])
df.to_csv(tsv_output_file, sep='\t', index=False)

print(f'Successfully converted and saved to {tsv_output_file}')


def update_tsv_with_key(tsv_file, key_file, output_file):
    # Read the .tsv file into a pandas DataFrame
    tsv_df = pd.read_csv(tsv_file, sep='\t')

    # Create a dictionary from the .key file
    key_dict = {}
    with open(key_file, 'r') as kf:
        for line in kf:
            parts = line.strip().split()
            if len(parts) >= 3:
                key_id = parts[0]
                bn_synset = parts[2]
                key_dict[key_id] = bn_synset

    # Add the new column 'BN Synset' to the DataFrame
    tsv_df['BN Synset'] = tsv_df.iloc[:, 0].map(key_dict)

    # Write the updated DataFrame back to a .tsv file
    tsv_df.to_csv(output_file, sep='\t', index=False)


# Example usage:
tsv_file = '../../data/Spanish/tokens_gold_Spanish.tsv'
key_file = '../../data/Spanish/semeval-2015-task-13-es.key'
output_file = '../../data/Spanish/gold-tokens-Spanish-wSenses.tsv'

update_tsv_with_key(tsv_file, key_file, output_file)

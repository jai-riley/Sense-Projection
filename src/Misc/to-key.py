import csv


# Function to parse and process the input TSV file
def process_tsv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
        open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile, delimiter='\t')
        writer = csv.DictWriter(outfile, fieldnames=['Start', 'Finish', 'BN Synset'], delimiter='\t')
        writer.writeheader()

        current_start = None
        current_finish = None

        for row in reader:
            token_id = row['Token ID IT']
            bn_synset = row['Sense IT']

            if '➕' in token_id:
                token_id = token_id.split('➕')
                current_finish = token_id[-1]
                current_start = token_id[0]
            else:
                current_start = token_id
                current_finish = token_id
            if bn_synset != "":
                writer.writerow({'Start': current_start, 'Finish': current_finish, 'BN Synset':bn_synset})


# Replace 'input.tsv' and 'output.tsv' with your file paths
process_tsv('../../data/Italian/tokens_aligned-Italian_sorted.tsv', '../../data/Italian/Italian-key.tsv')

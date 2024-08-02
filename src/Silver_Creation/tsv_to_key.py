import csv

def process_tsv(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
        open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile, delimiter='\t')
        writer = csv.DictWriter(outfile, fieldnames=['Start', "Sense"], delimiter=' ')
        writer.writeheader()
        for row in reader:
            token_id = row['Token ID']
            bn_synset = row['BN Synset']

            if '➕' in token_id:
                token_id = token_id.split('➕')
                current_start = token_id[0]
            else:
                current_start = token_id
            if bn_synset != "":
                bn_synset = bn_synset.split(";")
                d = {'Start': current_start, "Sense": bn_synset[0]}
                # for x in range(len(bn_synset)):
                #     d[f"Sense {x}"] = bn_synset[x]

                writer.writerow(d)



def process_key(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
        open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile, delimiter='\t')
        writer = csv.DictWriter(outfile, fieldnames=['Start', 'Sense 0','Sense 1','Sense 2','Sense 3','Sense 4','Sense 5','Sense 6','Sense 7','Sense 8','Sense 9','Sense 10','Sense 11','Sense 12','Sense 13','Sense 14','Sense 15','Sense 16','Sense 17','Sense 18','Sense 19','Sense 20'], delimiter=' ')
        writer.writeheader()

        for row in reader:
            token_id = row[0]
            bn_synset = row[2:]
            # print(bn_synset)
            current_start = token_id
            if bn_synset != "":

                d = {'Start': current_start}
                for x in range(len(bn_synset)):
                    d[f"Sense {x}"] = bn_synset[x]

                writer.writerow(d)


# Replace 'input.tsv' and 'output.tsv' with your file paths
# process_key(f'../../data/{language}/New_Ids/{language}-new-key.tsv', f'../../data/{language}/New_Ids/gold-key-{language}.txt')

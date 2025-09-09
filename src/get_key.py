import csv
import argparse

def make_key_file(input_tsv, output_txt, id_column="Token ID", synset_column="BN Synset"):
    """
    Reads a TSV file and writes a .txt file with two values per line:
    the ID and the Synset value, but only for rows where the Synset
    column is not empty.

    Parameters
    ----------
    input_tsv : str
        Path to the input TSV file.
    output_txt : str
        Path to the output TXT file.
    id_column : str, optional
        Name of the column containing the ID (default is "Token ID").
    synset_column : str, optional
        Name of the column containing the BN Synset value (default is "BN Synset").
    """
    try:
        with open(input_tsv, mode='r', newline='', encoding='utf-8') as tsv_file:
            reader = csv.DictReader(tsv_file, delimiter='\t')
            
            with open(output_txt, mode='w', encoding='utf-8') as txt_file:
                for row in reader:
                    synset = row.get(synset_column, "").strip()
                    if synset:  # only write non-empty synsets
                        id_value = row.get(id_column, "").strip()
                        txt_file.write(f"{id_value} {synset}\n")
                        
        print(f"Finished writing to {output_txt}")

    except FileNotFoundError:
        print(f"File {input_tsv} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a TSV file to a key TXT file with ID and Synset.")
    parser.add_argument("input_tsv", help="Path to the input TSV file")
    parser.add_argument("output_txt", help="Path to the output TXT file")
    parser.add_argument("--id_column", default="Token ID", help="Name of the ID column in the TSV (default: 'Token ID')")
    parser.add_argument("--synset_column", default="BN Synset", help="Name of the Synset column in the TSV (default: 'BN Synset')")

    args = parser.parse_args()

    make_key_file(args.input_tsv, args.output_txt, args.id_column, args.synset_column)

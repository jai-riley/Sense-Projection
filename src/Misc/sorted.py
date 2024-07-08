import pandas as pd

# Load the TSV file
input_file = '../../data/Italian/tokens_aligned-Italian.tsv'
output_file = '../../data/Italian/tokens_aligned-Italian_sorted.tsv'

# Read the TSV file into a DataFrame
df = pd.read_csv(input_file, sep='\t')

# Sort the DataFrame by 'Token ID ES'
df_sorted = df.sort_values(by='Token ID IT')

# Write the sorted DataFrame to a new TSV file
df_sorted.to_csv(output_file, sep='\t', index=False)

print(f'Successfully sorted and saved to {output_file}')

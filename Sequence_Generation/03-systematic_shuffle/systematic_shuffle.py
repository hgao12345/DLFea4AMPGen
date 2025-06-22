import itertools
import csv
import argparse

# Set up argparse
parser = argparse.ArgumentParser(description="Generate amino acid sequence combinations based on a CSV input file.")
parser.add_argument('--input_file', type=str, required=True, help='CSV file containing position and amino acid list')
parser.add_argument('--output_file', type=str, required=True, help='Output CSV file to save generated sequences')
parser.add_argument('--length', type=int, default=13, help='Peptide length (default: 13)')
args = parser.parse_args()

# Read amino acid composition from CSV
amino_acids = {}

with open(args.input_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        pos = int(row['position'])
        aa_list = row['amino_acids'].split(';')
        amino_acids[pos] = aa_list

# Generate sequences
sequences = []
for combo in itertools.product(*[amino_acids[i] for i in range(1, args.length + 1)]):
    sequence = ''.join(combo)
    sequences.append(sequence)

# Save sequences in FASTA format
with open(args.output_file, 'w') as f:
    for i, sequence in enumerate(sequences):
        f.write(f'>seq{i}\n{sequence}\n')

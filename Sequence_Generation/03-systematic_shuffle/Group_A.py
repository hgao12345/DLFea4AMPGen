import itertools
import csv
import os

# Amino acid composition at each position
amino_acids = {
    1: ['G', 'K', 'L'],
    2: ['G', 'K', 'L'],
    3: ['G', 'K', 'L'],
    4: ['G', 'K', 'L'],
    5: ['G', 'K', 'L'],
    6: ['G', 'K', 'L'],
    7: ['G', 'K', 'L'],
    8: ['G', 'K', 'L'],
    9: ['G', 'K', 'L'],
    10: ['A', 'K', 'L'],
    11: ['C', 'K', 'L'],
    12: ['G', 'K', 'L'],
    13: ['G', 'K', 'L']
}

# Generate sequences with different amino acid permutations
sequences = []

for combo in itertools.product(*[amino_acids[i] for i in range(1, 14)]):
    sequence = ''.join(combo)
    sequences.append(sequence)

with open('sequences_Agroup.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'sequence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i, sequence in enumerate(sequences):
        writer.writerow({'id': f'seq{i}', 'sequence': sequence})



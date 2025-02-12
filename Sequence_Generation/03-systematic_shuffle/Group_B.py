import itertools
import csv
import os

# Amino acid composition at each position
amino_acids = {
    1: ['G', 'K', 'L'],
    2: ['A', 'G', 'K'],
    3: ['G', 'K', 'L'],
    4: ['A', 'K', 'L'],
    5: ['A', 'K', 'L'],
    6: ['A', 'K', 'L'],
    7: ['A', 'G', 'K'],
    8: ['A', 'K', 'L'],
    9: ['A', 'K', 'L'],
    10: ['A', 'G', 'K'],
    11: ['A', 'K', 'L'],
    12: ['A', 'K', 'L'],
    13: ['G', 'K', 'L']
}

# Generate sequences with different amino acid permutations
sequences = []

for combo in itertools.product(*[amino_acids[i] for i in range(1, 14)]):
    sequence = ''.join(combo)
    sequences.append(sequence)

with open('sequences_Bgroup.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'sequence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i, sequence in enumerate(sequences):
        writer.writerow({'id': f'seq{i}', 'sequence': sequence})



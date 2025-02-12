import itertools
import csv
import os

# Amino acid composition at each position
amino_acids = {
    1: ['C', 'G', 'K'],
    2: ['G', 'K', 'L'],
    3: ['C', 'G', 'K'],
    4: ['C', 'G', 'K'],
    5: ['C', 'G', 'K'],
    6: ['C', 'G', 'K'],
    7: ['C', 'G', 'K'],
    8: ['C', 'G', 'K'],
    9: ['C', 'G', 'K'],
    10: ['C', 'G', 'L'],
    11: ['C', 'G', 'K'],
    12: ['C', 'G', 'K'],
    13: ['C', 'G', 'K']
}

# Generate sequences with different amino acid permutations
sequences = []

for combo in itertools.product(*[amino_acids[i] for i in range(1, 14)]):
    sequence = ''.join(combo)
    sequences.append(sequence)


with open('sequences_Cgroup.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'sequence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i, sequence in enumerate(sequences):
        writer.writerow({'id': f'seq{i}', 'sequence': sequence})


import itertools
import csv
import os

# Amino acid composition at each position
amino_acids = {
    1: ['I', 'K', 'R'],
    2: ['K', 'L', 'R'],
    3: ['K', 'P', 'R'],
    4: ['K', 'R', 'W'],
    5: ['K', 'P', 'R'],
    6: ['K', 'R', 'W'],
    7: ['K', 'P', 'R'],
    8: ['K', 'R', 'W'],
    9: ['K', 'R', 'W'],
    10: ['K', 'P', 'R'],
    11: ['K', 'R', 'W'],
    12: ['K', 'P', 'R'],
    13: ['K', 'P', 'R']
}

# Generate sequences with different amino acid permutations
sequences = []

for combo in itertools.product(*[amino_acids[i] for i in range(1, 14)]):
    sequence = ''.join(combo)
    sequences.append(sequence)


with open('sequences_Dgroup.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'sequence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i, sequence in enumerate(sequences):
        writer.writerow({'id': f'seq{i}', 'sequence': sequence})



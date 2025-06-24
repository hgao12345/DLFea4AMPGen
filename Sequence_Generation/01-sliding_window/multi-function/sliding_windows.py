import os
from statistics import mean
import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--SHAP_file', type=str, required=True, help='TXT file containing SHAP values')
parser.add_argument('--seq_file', type=str, required=True, help='The original file for calculating SHAP values')
parser.add_argument('--length', type=int, required=True, help='Sliding window size (integer value)')
parser.add_argument('--output_path', type=str, required=True, help='Directory path to save the result file')

args = parser.parse_args()

# Read the sequence and SHAP data into DataFrames
id_from = pd.read_csv(args.seq_file)
shap_ = pd.read_table(args.SHAP_file, header=None, names=['shap_value'])

# Merge file 1 and file 2 by column
merged_df = pd.concat([id_from, shap_], axis=1)

# Filter rows with a string length greater than or equal to the setting length in a certain column
filtered_df_len = merged_df[merged_df['seq'].str.len() >= args.length]

print(filtered_df_len)

df = pd.DataFrame(columns=['id', 'seq', 'shap_value'])

for line in range(len(filtered_df_len)):
    filtered_df_1 = filtered_df_len.iloc[line,:]

    ## The first sequence
    id_ = filtered_df_1["id"]
    seq_ = filtered_df_1["seq"]
    shap_value_0 = filtered_df_1["shap_value"]

    shap_value_1 = list(shap_value_0.split(","))
    shap_value_2 = [float(item) for item in shap_value_1][1:-1]
    mean_seq_shap = mean(shap_value_2)
    print(mean_seq_shap)

    max_sum_seqlets = -float('inf')
    max_seq_cut = ""
    max_shap_cut_str = ""

    l = args.length - 1
    ## Cut every window, where all+1 values are due to the inability to retrieve data on the right side
    for pos_left in range(len(seq_) - l):
        pos_right = pos_left + l
        seq_cut = seq_[pos_left:pos_right + 1]
        shap_cut = shap_value_2[pos_left:pos_right + 1]
        sorted_list = sorted(shap_cut, reverse=True)

        sum_seqlets = sum(shap_cut)

        if sum_seqlets > 0:
            if sum_seqlets > max_sum_seqlets:
                max_sum_seqlets = sum_seqlets
                max_seq_cut = seq_cut
                shap_cut_str0 = [str(item) for item in shap_cut]
                max_shap_cut_str = ",".join(shap_cut_str0)

    if max_seq_cut != "":
        id_n = f"{id_}_{pos_left}"
        my_list = [id_n, max_seq_cut, max_shap_cut_str]
        df.loc[len(df)] = my_list

# Save output to the specified directory
df.to_csv(f"{args.output_path}/{args.length}AA_motif.csv", index=False)

# Also write the sequences to a FASTA file
fasta_path = os.path.join(args.output_path, f"{args.length}AA_motif.fasta")
with open(fasta_path, "w") as fasta_file:
    for i in range(len(df)):
        fasta_file.write(f">{df.loc[i, 'id']}\n{df.loc[i, 'seq']}\n")

print("DONE!!!")

import os
from statistics import mean
import pandas as pd
import numpy as np

id_from = pd.read_csv("3model_inner_data.csv")
shap_ = pd.read_table("all_3model_mean.txt")
# Merge file 1 and file 2 by column
merged_df = pd.concat([id_from, shap_], axis=1)

# Filter rows with a string length greater than or equal to 13 in a certain column
filtered_df_len = merged_df[merged_df['seq'].str.len() >= 13]

df = pd.DataFrame(columns=['id', 'seq', 'shap_value'])

for line in range(len(filtered_df_len)):
    
    shap_i = filtered_df_len.iloc[line,:]
    

    filtered_df_1 = shap_i

    ## The first sequence
    id_ = filtered_df_1["id"]
    seq_ = filtered_df_1["seq"]
    shap_value_0 = filtered_df_1["shap_value"]

    shap_value_1 = list(shap_value_0.split(","))
    shap_value_2 = [float(item) for item in shap_value_1][1:-1] #不用取负因为标准化的时候取过了
    mean_seq_shap = mean(shap_value_2)
    print(mean_seq_shap)

    max_sum_seqlets = -float('inf') 
    max_seq_cut = ""
    max_shap_cut_str = ""

    ## Cut every 13AA, where all+1 values are due to the inability to retrieve data on the right side
    for pos_left in range(len(seq_) - 12):
        pos_right = pos_left + 12
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

df.to_csv("13AA_motif_dayu_0_right.csv",index=None)

print("DONE!!!")
















    
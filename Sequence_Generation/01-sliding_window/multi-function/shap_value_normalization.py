import os
import pandas as pd
import sys

f16 = open("ABP_shap_value_3model_inner.txt","r",encoding="utf-8")
f17 = open("AFP_shap_value_3model_inner.txt","r",encoding="utf-8")
f20 = open("AOP_shap_value_3model_inner.txt","r",encoding="utf-8")

normalized_list16_right = open("normalized_ABP.txt","a",encoding="utf-8")
normalized_list17_right = open("normalized_AFP.txt","a",encoding="utf-8")
normalized_list20_right = open("normalized_AOP.txt","a",encoding="utf-8")
all_3model_mean_right = open("all_3model_mean.txt","a",encoding="utf-8")

for i,ii,iii in zip(f16.readlines(),f17.readlines(),f20.readlines()):
    line16_ = i.strip().split(", ")
    line17_ = ii.strip().split(", ")
    line20_ = iii.strip().split(", ")
    line16 = [-float(item) for item in line16_]
    line17 = [-float(item) for item in line17_]
    line20 = [-float(item) for item in line20_]
    # Standardize each element in the list
    normalized_list16_values = [(x-0)/(18.428-0) if x > 0 else x / (9.521) for x in line16]
    normalized_list17_values = [(x-0)/(19.021-0) if x > 0 else x / (9.639) for x in line17]
    normalized_list20_values = [(x-0)/(15.071-0) if x > 0 else x / (7.846) for x in line20]
    added_list = [x + y + z for x, y, z in zip(normalized_list16_values, normalized_list17_values, normalized_list20_values)]

    # Convert the list to a string
    normalized_list16_str = ', '.join(map(str, normalized_list16_values))
    normalized_list17_str = ', '.join(map(str, normalized_list17_values))
    normalized_list20_str = ', '.join(map(str, normalized_list20_values))
    all_3model_mean_str = ', '.join(map(str, added_list))

    
    with open("normalized_ABP.txt", "a") as file_normalized_list16:
        file_normalized_list16.write(f"{normalized_list16_str}\n")
    with open("normalized_AFP", "a") as file_normalized_list17:
        file_normalized_list17.write(f"{normalized_list17_str}\n")
    with open("normalized_AOP.txt", "a") as file_normalized_list20:
        file_normalized_list20.write(f"{normalized_list20_str}\n")
    with open("all_3model_mean_right.txt", "a") as file_all_3model_mean:
        file_all_3model_mean.write(f"{all_3model_mean_str}\n")

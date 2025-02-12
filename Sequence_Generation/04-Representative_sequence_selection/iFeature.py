# Environment Configuration: https://github.com/Superzchen/iFeature/

import os
import sys
from collections import Counter

import pandas as pd
import iFeatureOmegaCLI
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist

from pylab import *
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from yellowbrick.cluster.elbow import kelbow_visualizer
from yellowbrick.datasets.loaders import load_nfl

def name_seq(fasta_file):
    with open(fasta_file, 'r') as file:
        lines = file.readlines()
    name_list, seq_list = [], []
    for line in lines:
        if '>' in line:
            name_list.append(line.strip().replace('>', ''))
            seq_list.append('')
        else:
            seq_list[-1] = '%s%s' % (seq_list[-1], line.strip().upper())
    return name_list, seq_list


# in_para = sys.argv[1:]
in_para = ["example.fasta"]  # sys.argv[1:]

name_list, seq_list = name_seq(in_para[0])
seq_elements = list(Counter(''.join(seq_list)))


abs_path = "~/anaconda3/lib/python3.7/site-packages/iFeatureOmegaCLI"

if len(seq_elements) < 10:
    if len(in_para) == 1:
        in_file = in_para[0]
        feature_types_index = 0
    else:
        in_file = in_para[0]
        feature_types_index = int(in_para[1])
    print(len(in_para))

    print("\t* Using DNA-para.json!!!")
    json_file = f'{abs_path}/parameters/DNA_parameters_setting.json'

    ##########################################################
    dna = iFeatureOmegaCLI.iDNA(in_file)

    feature_types = dna.display_feature_types()
    use_feature_types = feature_types[feature_types_index]
    print(f"\t* use_feature_types = {use_feature_types}")

    save_csv_path = f"./{'.'.join(in_file.split('.')[:-1])}__{use_feature_types.replace(' ', '-')}.csv"
    
    if os.path.exists(save_csv_path) is False:
        dna.import_parameters(json_file)
        dna.get_descriptor(use_feature_types)
        print(dna.encodings)

        dna.to_csv(save_csv_path, "index=False", header=False)
    
else:
    if len(in_para) == 1:
        in_file = in_para[0]
        feature_types_index = 31
    else:
        in_file = in_para[0]
        feature_types_index = int(in_para[1])
    print(len(in_para))

    print("\t* Using Protein-para.json!!!")
    json_file = f'{abs_path}/parameters/Protein_parameters_setting.json'

    ############################################################
    prot = iFeatureOmegaCLI.iProtein(in_file)

    feature_types = prot.display_feature_types()
    # feature_types.index("PAAC")
    use_feature_types = feature_types[feature_types_index]
    print(f"\t* use_feature_types = {use_feature_types}")

    
    save_csv_path = f"./{'.'.join(in_file.split('.')[:-1])}__{use_feature_types.replace(' ', '-')}.csv"

    if os.path.exists(save_csv_path) is False:
        prot.import_parameters(json_file)
        prot.get_descriptor(use_feature_types)
        print(prot.encodings)

        prot.to_csv(save_csv_path, "index=False", header=False)



dimension_reduction_csv_path = f"{'.'.join(save_csv_path.split('.')[:-1])}__PCA.csv"
if os.path.exists(dimension_reduction_csv_path) is False:
    df0 = pd.read_csv(save_csv_path, sep=',', header=None, index_col=0)
    pca_data = iFeatureOmegaCLI.iAnalysis(df0)
    pca_data.ZScore()
    pca_data.PCA(n_components=3, in_random_state=100)
    pca_data.dimension_to_csv(file=dimension_reduction_csv_path)

plot_df_dim = pd.read_csv(dimension_reduction_csv_path, sep=',', header=None, index_col=False)
dig = plot_df_dim.values.T
explain_x, explain_y = dig[0][0], dig[1][0]
dig_x, dig_y = dig[0][1:], dig[1][1:]



df1 = pd.read_csv(save_csv_path, sep=',', header=None, index_col=0)
X = df1.values


colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
for cluster_num in range(2, 9):
    print(cluster_num, flush=True)

    cluster_csv_path = f"{'.'.join(save_csv_path.split('.')[:-1])}__kmeans{cluster_num}.csv"

    if os.path.exists(cluster_csv_path) is False:
        df1 = pd.read_csv(save_csv_path, sep=',', header=None, index_col=0)
        kmeans_data = iFeatureOmegaCLI.iAnalysis(df1)
        kmeans_data.ZScore()
        # cluster_num = 4
        kmeans_data.kmeans(nclusters=cluster_num, in_random_state=100)
        kmeans_data.cluster_to_csv(file=cluster_csv_path)


    plot_df_kmeans = pd.read_csv(cluster_csv_path, sep=',', index_col=False)
    seq_name, c_num = plot_df_kmeans.values.T
    # plot_color = [f"C{num}" for num in c_num]
    plot_color = [colors[num] for num in c_num]

    x, y = dig_x, dig_y
    rcParams["axes.prop_cycle"]
    fig = plt.figure(figsize=(16, 16))
    plt.style.use('ggplot')
    G = gridspec.GridSpec(100, 100)

    ax_all = subplot(G[26:69, 5:63])
    

    #######################################################
    for name, xi, yi in zip(seq_name, x, y):
        if "C_Yes" in name:
            plt.scatter(xi, yi, c="k", edgecolors="k", s=180, alpha=.6)
            plt.scatter(xi, yi, c="w", edgecolors="k", s=80)
        # elif name.startswith("CS"):
        #     plt.scatter(xi, yi, c="k", edgecolors="k", s=180, alpha=.6)
        #     plt.scatter(xi, yi, c="w", edgecolors="k", s=80)
    #######################################################

    plt.scatter(x, y, c=plot_color, s=80, alpha=.6)

    for color_num in range(cluster_num):
        plt.scatter(100, 100, c=colors[color_num], label="Cluster{:d}({:,d})".format(color_num, Counter(c_num).get(color_num)), s=90)
    plt.xlim(min(x)*1.1, max(x)*1.2)
    plt.ylim(min(y)*1.1, max(y)*1.1)
    plt.legend(fontsize=16, loc='upper right', frameon=True, fancybox=True, facecolor="w")
    plt.xticks(fontsize=16, weight="bold")
    plt.yticks(fontsize=16, weight="bold")
    plt.xlabel(f"PCA-1  ({round(explain_x*100, 2)}% Explained)", fontsize=20, weight="bold")
    plt.ylabel(f"PCA-2  ({round(explain_y*100, 2)}% Explained)", fontsize=20, weight="bold")

        
    clstr_num = list(Counter(c_num))
    for ax_i in clstr_num:
        if ax_i < 3:
            sub_ax = subplot(G[:23, 33*ax_i:31+33*ax_i])
        elif 3 <= ax_i < 5:
            sub_ax = subplot(G[25+25*(ax_i-3):48+25*(ax_i-3), 66:97])
        elif 5 <= ax_i < 8:
            sub_ax = subplot(G[75:98, 33*(ax_i-5):31+33*(ax_i-5)])

        p_x, p_y, bc_x, bc_y = [], [], [], []
        for x_, y_, c_ in zip(x, y, c_num):
            if c_ == ax_i:
                p_x.append(x_)
                p_y.append(y_)
            else:
                bc_x.append(x_)
                bc_y.append(y_)
        
        #######################################################
        for name, xi, yi in zip(seq_name, x, y):
            if "C_Yes" in name:
                plt.scatter(xi, yi, c="k", edgecolors="k", s=180, alpha=.6)
                plt.scatter(xi, yi, c="w", edgecolors="k", s=80)
        #######################################################
        
        plt.scatter(np.array(bc_x), np.array(bc_y), c="lightgray", s=60, alpha=.6, zorder=0)
        plt.scatter(np.array(p_x), np.array(p_y), c=colors[ax_i], s=60, alpha=.6, zorder=2, label=f"Cluster{ax_i}")
        
        plt.legend(fontsize=16, loc='upper right', frameon=True, fancybox=True, facecolor="w")
        plt.xlim(min(x)*1.1, max(x)*1.2)
        plt.ylim(min(y)*1.1, max(y)*1.1)


    for ax_i in range(len(clstr_num), 8):
        if ax_i < 3:
            sub_ax = subplot(G[:23, 33*ax_i:31+33*ax_i])
        elif 3 <= ax_i < 5:
            sub_ax = subplot(G[25+25*(ax_i-3):48+25*(ax_i-3), 66:97])
        elif 5 <= ax_i < 8:
            sub_ax = subplot(G[75:98, 33*(ax_i-5):31+33*(ax_i-5)])

        plt.xticks([])
        plt.yticks([])

    plt.savefig(f"{'.'.join(dimension_reduction_csv_path.split('.')[:-1])}__k{cluster_num}.png", format="png", dpi=330)


fig_kn = plt.figure()
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel("k", fontsize=17, weight="bold")
plt.ylabel("x", fontsize=17, weight="bold")
plot_info = kelbow_visualizer(KMeans(random_state=100), X, k=(2,9))
plt.yticks(fontsize=15)
plt.ylabel("Fit time (seconds)", fontsize=17, weight="bold")
plt.savefig(f"{'.'.join(save_csv_path.split('.')[:-1])}__kmeans.png", bbox_inches="tight", format="png", dpi=330)

print("Done!!!")

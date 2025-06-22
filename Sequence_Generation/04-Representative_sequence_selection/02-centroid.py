from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import argparse
import os

# Set up argparse
parser = argparse.ArgumentParser(description="Perform KMeans clustering on example data.")
parser.add_argument('--input_file', type=str, required=True, help='Input CSV file (e.g., example_data.csv)')
parser.add_argument('--output_path', type=str, required=True, help='Directory to save output files')
parser.add_argument('--random_seed', type=int, default=1, help='Random seed for KMeans (default: 1)')
parser.add_argument('--n_clusters', type=int, default=4, help='Number of clusters (default: 4)')
args = parser.parse_args()

# Ensure output directory exists
os.makedirs(args.output_path, exist_ok=True)

# Load data
data = pd.read_csv(args.input_file, header=0)

# Extract data for clustering (assumes 2nd and 3rd columns are numeric features)
data_for_clustering = data.iloc[:, 1:3].values

# Perform KMeans clustering
kmeans = KMeans(n_clusters=args.n_clusters, random_state=args.random_seed)
kmeans.fit(data_for_clustering)
data['cluster'] = kmeans.labels_

# Save each cluster's data and write closest point to text
output_info_path = os.path.join(args.output_path, f"seed{args.random_seed}_example_cluster_info.txt")
with open(output_info_path, 'w') as file:
    for cluster_num in range(kmeans.n_clusters):
        cluster_data = data[data['cluster'] == cluster_num]
        cluster_filename = os.path.join(args.output_path, f"seed{args.random_seed}_example_cluster_{cluster_num}.csv")
        cluster_data.to_csv(cluster_filename, index=False)

        center = kmeans.cluster_centers_[cluster_num]
        distances = np.linalg.norm(cluster_data.iloc[:, 1:3].values - center, axis=1)
        min_distance_index = np.argmin(distances)
        closest_row = cluster_data.iloc[min_distance_index]

        # Print and write closest sequence
        msg = f"Cluster {cluster_num} - Closest sequence ID: {closest_row[3]}, Sequence: {closest_row[4]}"
        print(msg)
        file.write(msg + "\n")

print(f"\nCluster info saved to: {output_info_path}")
print("All cluster data files saved successfully.")

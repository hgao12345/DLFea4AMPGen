from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import os

data = pd.read_csv("example_data.csv", header=0)

# Data for KMeans clustering (assuming columns 2 and 3)
data_for_clustering = data.iloc[:, 1:3].values

# Create KMeans instance, set number of clusters to 4, and specify random seed
random_seed = 1
kmeans = KMeans(n_clusters=4, random_state=random_seed)

# Fit the model
kmeans.fit(data_for_clustering)

# Get cluster labels for each data point
labels = kmeans.labels_

# Add cluster labels to the original DataFrame
data['cluster'] = labels

# Group data by clusters and save each cluster's data to a CSV file
for cluster_num in range(kmeans.n_clusters):
    # Extract data for the corresponding cluster, including ID and sequence
    cluster_data = data[data['cluster'] == cluster_num]

    # Save cluster data to CSV, including ID and sequence
    cluster_data.to_csv(f"seed{random_seed}_example_cluster_{cluster_num}.csv", index=False)
    
    # Calculate the distance of each point from the cluster center
    center = kmeans.cluster_centers_[cluster_num]
    distances = np.linalg.norm(cluster_data.iloc[:, 1:3].values - center, axis=1)

    # Find the point closest to the cluster center
    min_distance_index = np.argmin(distances)
    closest_row = cluster_data.iloc[min_distance_index]

    # Print the information of the sequence closest to the cluster center
    print(f"Cluster {cluster_num} - Closest sequence ID: {closest_row[3]}, Sequence: {closest_row[4]}")

# Create a text file to write the output
with open(f"seed{random_seed}_example_cluster_info.txt", 'w') as file:
    for cluster_num in range(kmeans.n_clusters):
        cluster_data = data[data['cluster'] == cluster_num]
        center = kmeans.cluster_centers_[cluster_num]
        distances = np.linalg.norm(cluster_data.iloc[:, 1:3].values - center, axis=1)
        min_distance_index = np.argmin(distances)
        closest_row = cluster_data.iloc[min_distance_index]

        # Write the information of the closest sequence to the cluster center into the file
        file.write(f"Cluster {cluster_num} - Closest sequence ID: {closest_row[3]}, Sequence: {closest_row[4]}\n")

print("Cluster information has been saved to the text file.")

print("Data has been grouped by clusters and saved. Each file contains the corresponding ID and sequence.")

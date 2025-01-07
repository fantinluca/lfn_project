import pandas as pd
import os, sys
import networkx as nx
from time import time

import create_graphs, compute_metrics

starting_time = int(str(time()).replace(".",""))

# --- Generate Random Graphs and Calculate Metrics ---
# Parameters for the Power Law Clustered Graph
n = 10 # Number of nodes (1/50 of the real graph)
m = 2  # Number of edges to add for each new node
p = 0.3  # Clustering probability

# Specify the number of random graphs to generate
num_random_graphs = int(sys.argv[1])  # Change this value to generate more or fewer random graphs

graph_metrics_data = []

result_dir = os.path.dirname(__file__)
result_dir = result_dir.replace("src", "results")

for i in range(num_random_graphs):
    seed = int(str(time()).replace(".",""))

    # create graph
    print(f"Creating Random Graph {i+1}/{num_random_graphs}...")
    random_graph = nx.powerlaw_cluster_graph(n, m, p, seed=seed)

    # compute metrics for graph
    graph_metrics, node_metrics = compute_metrics.compute_all_metrics(random_graph)
    print(f"Computed metrics for graph {i+1}")
    
    # add graph metrics to graph_metrics_data
    tmp = {
        "graph": seed,
        **graph_metrics
    }
    graph_metrics_data.append(tmp)

    # save node metrics to csv
    metrics_df = pd.DataFrame(node_metrics)
    output_file = os.path.join(result_dir, f"random_graph_{seed}_node_metrics.csv")
    metrics_df.to_csv(output_file, sep=";", index=False)
    print(f"All metrics for graph {seed} saved to {output_file}.")

# save graph metrics to csv file
metrics_df = pd.DataFrame(graph_metrics_data)
output_file = os.path.join(result_dir, f"graph_metrics_{starting_time}.csv")
metrics_df.to_csv(output_file, index=False)
print(f"All metrics saved to {output_file}.")

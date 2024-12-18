import pandas as pd
import os, sys
import networkx as nx

import read_real_graph

# --- Generate Random Graphs and Calculate Metrics ---
# Parameters for the Power Law Clustered Graph
n = read_real_graph.get_size()/50  # Number of nodes (1/50 of the real graph)
m = 2  # Number of edges to add for each new node
p = 0.3  # Clustering probability

# Specify the number of random graphs to generate
num_random_graphs = int(sys.argv[1])  # Change this value to generate more or fewer random graphs

all_metrics_data = []

for i in range(num_random_graphs):
    print(f"Creating Random Graph {i+1}/{num_random_graphs}...")
    random_graph = nx.powerlaw_cluster_graph(n, m, p, seed=i)

    # --- Connected Components ---
    connected_components = list(nx.connected_components(random_graph))
    num_connected_components = len(connected_components)
    print(f"Random Graph {i+1}: Number of connected components: {num_connected_components}")

    # --- Calculate Average Clustering Coefficient ---
    clustering_coefficient = nx.average_clustering(random_graph)
    print(f"Random Graph {i+1}: Average clustering coefficient: {clustering_coefficient}")

    # --- Calculate Centrality Metrics ---
    # Degree Centrality
    degree_centrality = nx.degree_centrality(random_graph)
    print(f"Random Graph {i+1}: Degree centrality calculated.")

    # Closeness Centrality
    closeness_centrality = nx.closeness_centrality(random_graph)
    print(f"Random Graph {i+1}: Closeness centrality calculated.")

    # Betweenness Centrality
    betweenness_centrality = nx.betweenness_centrality(random_graph)
    print(f"Random Graph {i+1}: Betweenness centrality calculated.")

    # PageRank
    pagerank = nx.pagerank(random_graph)
    print(f"Random Graph {i+1}: PageRank calculated.")

    # Eigenvector Centrality
    eigenvector_centrality = nx.eigenvector_centrality(random_graph, max_iter=1000, tol=1e-06)
    print(f"Random Graph {i+1}: Eigenvector centrality calculated.")

    # --- Collect Metrics ---
    for node in random_graph.nodes():
        all_metrics_data.append({
            "random_graph": i + 1,
            "node": node,
            "degree_centrality": degree_centrality.get(node, 0),
            "closeness_centrality": closeness_centrality.get(node, 0),
            "betweenness_centrality": betweenness_centrality.get(node, 0),
            "pagerank": pagerank.get(node, 0),
            "eigenvector_centrality": eigenvector_centrality.get(node, 0)
        })

# Save all metrics to a single CSV file
result_dir = os.path.dirname(__file__)
result_dir = result_dir.replace("src", "results")
metrics_df = pd.DataFrame(all_metrics_data)
output_file = os.path.join(result_dir, "all_random_graphs_metrics.csv")
metrics_df.to_csv(output_file, index=False)
print(f"All metrics saved to {output_file}.")

import pandas as pd
import os
import networkx as nx
import random

# Gets the current directory where the script is located
current_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset")

# Builds full paths to .csv files within the current directory
nodes_path = os.path.join(current_dir, 'nodes.csv')
edges_path = os.path.join(current_dir, 'edges.csv')

# Load the entire CSV files (without row limit)
os.system('cls')
print("Loading nodes and edges CSV files...")
nodes_df = pd.read_csv(nodes_path)  # Without limit
edges_df = pd.read_csv(edges_path)  # Without limit
print("CSV files loaded successfully.")

# Create the Graph from the real dataset
os.system('cls')
print("Creating the real graph from the dataset...")
G = nx.Graph()

# Add nodes to the graph
for index, row in nodes_df.iterrows():
    G.add_node(row['spotify_id'], name=row['name'], followers=row['followers'],
               popularity=row['popularity'], genres=row['genres'], chart_hits=row['chart_hits'])
    if index % 100 == 0:  # Print progress every 100 nodes
        os.system('cls')
        print(f"Adding node {index+1}/{len(nodes_df)}")

# Add edges to the graph
for index, row in edges_df.iterrows():
    G.add_edge(row['id_0'], row['id_1'])
    if index % 100 == 0:  # Print progress every 100 edges
        os.system('cls')
        print(f"Adding edge {index+1}/{len(edges_df)}")

print(f"Real graph created with {len(G.nodes())} nodes and {len(G.edges())} edges.")

# --- Calculate Metrics for the Real Graph ---
print("Calculating metrics for the real graph...")
# Connected Components
connected_components_real = list(nx.connected_components(G))
num_connected_components_real = len(connected_components_real)
print(f"Real Graph: Number of connected components: {num_connected_components_real}")

# Average Clustering Coefficient
clustering_coefficient_real = nx.average_clustering(G)
print(f"Real Graph: Average clustering coefficient: {clustering_coefficient_real}")

# Degree Centrality
degree_centrality_real = nx.degree_centrality(G)
print(f"Real Graph: Degree centrality calculated.")

# Closeness Centrality
closeness_centrality_real = nx.closeness_centrality(G)
print(f"Real Graph: Closeness centrality calculated.")

# Betweenness Centrality
betweenness_centrality_real = nx.betweenness_centrality(G)
print(f"Real Graph: Betweenness centrality calculated.")

# PageRank
pagerank_real = nx.pagerank(G)
print(f"Real Graph: PageRank calculated.")

# Eigenvector Centrality
eigenvector_centrality_real = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
print(f"Real Graph: Eigenvector centrality calculated.")

# Collect Metrics for the Real Graph
all_metrics_data = []
for node in G.nodes():
    all_metrics_data.append({
        "random_graph": 0,  # 0 indicates the real graph
        "node": node,
        "degree_centrality": degree_centrality_real.get(node, 0),
        "closeness_centrality": closeness_centrality_real.get(node, 0),
        "betweenness_centrality": betweenness_centrality_real.get(node, 0),
        "pagerank": pagerank_real.get(node, 0),
        "eigenvector_centrality": eigenvector_centrality_real.get(node, 0)
    })

# --- Generate Random Graphs and Calculate Metrics ---
# Parameters for the Power Law Clustered Graph
n = len(G.nodes())/50  # Number of nodes (1/50 of the real graph)
m = 2  # Number of edges to add for each new node
p = 0.3  # Clustering probability

# Specify the number of random graphs to generate
num_random_graphs = 2  # Change this value to generate more or fewer random graphs

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
metrics_df = pd.DataFrame(all_metrics_data)
output_file = os.path.join(current_dir, "all_random_graphs_metrics.csv")
metrics_df.to_csv(output_file, index=False)
print(f"All metrics saved to {output_file}.")

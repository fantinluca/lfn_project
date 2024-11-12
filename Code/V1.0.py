import pandas as pd
import os
import networkx as nx

# Gets the current directory where the script is located
current_dir = os.path.dirname(__file__)

# Builds full paths to .csv files within the current directory
nodes_path = os.path.join(current_dir, 'nodes.csv')
edges_path = os.path.join(current_dir, 'edges.csv')

# Upload CSV files using paths relative to the current directory, limited to a subset of rows
nodes_df = pd.read_csv(nodes_path, nrows=1000)  #limite 1.000 nodi
edges_df = pd.read_csv(edges_path, nrows=1000)  #limite 1.000 edges

print("Colonne di nodes.csv:", nodes_df.columns)

print("Prime 20 righe di nodes.csv:")
print(nodes_df.head(20))

print("\nPrime 20 righe di edges.csv:")
print(edges_df.head(20))

# Create Graph
G = nx.Graph()

# Add nodes on the graph
for index, row in nodes_df.iterrows():
    G.add_node(row['spotify_id'], name=row['name'], followers=row['followers'],
               popularity=row['popularity'], genres=row['genres'], chart_hits=row['chart_hits'])

# Add edges on the graph (limited to the first 10,000 edges)
for index, row in edges_df.iterrows():
    G.add_edge(row['id_0'], row['id_1'])

# Centrality Measures and display top 10 nodes for each
# Degree Centrality
degree_centrality = nx.degree_centrality(G)
top_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Degree Centrality:")
for node, centrality in top_degree_centrality:
    print(f"Node: {node}, Degree Centrality: {centrality}")

# Closeness Centrality
closeness_centrality = nx.closeness_centrality(G)
top_closeness_centrality = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Closeness Centrality:")
for node, centrality in top_closeness_centrality:
    print(f"Node: {node}, Closeness Centrality: {centrality}")

# Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G)
top_betweenness_centrality = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Betweenness Centrality:")
for node, centrality in top_betweenness_centrality:
    print(f"Node: {node}, Betweenness Centrality: {centrality}")

# PageRank
pagerank = nx.pagerank(G) 
top_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 PageRank:")
for node, rank in top_pagerank:
    print(f"Node: {node}, PageRank: {rank}")

# Eigenvector Centrality
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
top_eigenvector_centrality = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Eigenvector Centrality:")
for node, centrality in top_eigenvector_centrality:
    print(f"Node: {node}, Eigenvector Centrality: {centrality}")

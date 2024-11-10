import pandas as pd
import os
import networkx as nx

# Gets the current directory where the script is located
current_dir = os.path.dirname(__file__)

# Builds full paths to .csv files within the current directory
nodes_path = os.path.join(current_dir, 'nodes.csv')
edges_path = os.path.join(current_dir, 'edges.csv')

# Upload CSV files using paths relative to the current directory
nodes_df = pd.read_csv(nodes_path)
edges_df = pd.read_csv(edges_path)


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

# Add arches on the graph
for index, row in edges_df.iterrows():
    G.add_edge(row['id_0'], row['id_1'])

# Centrality Measures
degree_centrality = nx.degree_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
pagerank = nx.pagerank(G) 


print("\nDegree Centrality:")
print(degree_centrality)

print("\nCloseness Centrality:")
print(closeness_centrality)

print("\nBetweenness Centrality:")
print(betweenness_centrality)

print("\nPageRank:")
print(pagerank)

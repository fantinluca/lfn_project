import pandas as pd
import os
import networkx as nx
import re


# Gets the current directory where the script is located
current_dir = os.path.dirname(__file__)
#print(current_dir)
current_dir = current_dir.replace("src", "dataset")

# Builds full paths to .csv files within the current directory
nodes_path = os.path.join(current_dir, 'nodes.csv')
edges_path = os.path.join(current_dir, 'edges.csv')

# Upload CSV files using paths relative to the current directory, limited to a subset of rows
nodes_df = pd.read_csv(nodes_path)
edges_df = pd.read_csv(edges_path)

# genre that will be considered
#genre = "hip hop"
#genre = "k-pop"
genre = "classical"


# Create Graph
G = nx.Graph()

# Add nodes on the graph
for index, row in nodes_df.iterrows():
    # a node will be added only if it contains the genre
    regexList = re.findall(r'\'(.*?)\'', row['genres'])
    # if it contains the genre
    if ( genre in regexList  ):
        G.add_node(row['spotify_id'], name=row['name'], followers=row['followers'],
               popularity=row['popularity'], genres=row['genres'], chart_hits=row['chart_hits'])


# Add edges on the graph
for index, row in edges_df.iterrows():
    # add the edge only if both nodes are in the graph
    if ( row['id_0'] in G and row['id_1'] in G ):
        G.add_edge(row['id_0'], row['id_1'])


# Print the number of nodes and edges
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")


# print the genre of every node in G
for node, data in G.nodes(data=True):
    print(f"Node {node}: Genres = {data.get('genres')}")


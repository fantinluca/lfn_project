# Questo file serve per ricercare un certo artista per ID
# cercherà inoltre tutti gli edge con quel nodo e dirà qual è l'altro artista
import pandas as pd
import os
import networkx as nx
import networkit as nk


#node_id = "3TtENHJRmw5dDe3fskI7cF" #Johann Bach
node_id = "1JOQXgYdQV2yfrhewqx96o" #Giuseppe Verdi


# Gets the current directory where the script is located
current_dir = os.path.dirname(__file__)
current_dir = current_dir.replace("src", "dataset")

# Builds full paths to .csv files within the current directory
nodes_path = os.path.join(current_dir, 'nodes.csv')
edges_path = os.path.join(current_dir, 'edges.csv')

# Upload CSV files using paths relative to the current directory, limited to a subset of rows
nodes_df = pd.read_csv(nodes_path)#, nrows=1000)  #limite 1.000 nodi
edges_df = pd.read_csv(edges_path)#, nrows=1000)  #limite 1.000 edges

# Create Graph
G = nx.Graph()

# Add nodes on the graph
for index, row in nodes_df.iterrows():
    G.add_node(row['spotify_id'], name=row['name'], followers=row['followers'],
               popularity=row['popularity'], genres=row['genres'], chart_hits=row['chart_hits'])

# Add edges on the graph (limited to the first 10,000 edges)
for index, row in edges_df.iterrows():
    G.add_edge(row['id_0'], row['id_1'])


# print the details of the node
if node_id in G.nodes:
    node_details = G.nodes[node_id]
    print(f"Node ID: {node_id}")
    print("Node Details:")
    for attribute, value in node_details.items():
        print(f"  {attribute}: {value}")
else:
    print(f"Node {node_id} not found in the graph.")



#  search in all the edges if this ID is present
# Print edges containing the specified node
print(f"Edges containing node {node_id}:")
for edge in G.edges(node_id):
    # Each edge is a tuple (node1, node2), check for the other node
    other_node = edge[1] if edge[0] == node_id else edge[0]
    
    # Get the details of the other node
    other_node_details = G.nodes[other_node]
    
    print(f"Edge: {edge} - Other Node ({other_node}) Details:")
    for attribute, value in other_node_details.items():
        print(f"  {attribute}: {value}")

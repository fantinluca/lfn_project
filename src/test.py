from create_graphs import create_popularity_percent_subgraph
import os
import pandas as pd


# I wanna compute the top 1%
thresh = 0.1

# Gets the current directory where the script is located
current_dir = os.path.dirname(__file__)
current_dir = current_dir.replace("src", "dataset")

# Builds full paths to .csv files within the current directory
nodes_path = os.path.join(current_dir, 'nodes.csv')
edges_path = os.path.join(current_dir, 'edges.csv')

# Upload CSV files using paths relative to the current directory, limited to a subset of rows
nodes_df = pd.read_csv(nodes_path)#, nrows=1000)  #limite 1.000 nodi
edges_df = pd.read_csv(edges_path)#, nrows=1000)  #limite 1.000 edges


G = create_popularity_percent_subgraph (nodes_df, edges_df, thresh)

print (f"Created subgraph with {thresh}% most popular artists ")

# Get the number of nodes
num_nodes = G.number_of_nodes()
print("Number of nodes:", num_nodes)

# Get the number of edges
num_edges = G.number_of_edges()
print("Number of edges:", num_edges)

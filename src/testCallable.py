from subgraphs import createPopularityThreshGraph
from subgraphs import createGenreGraph
import os
import pandas as pd


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


# only artists with popularity greater than this number will be considered
popularityThreshold = 80

#create graph only considering nodes with a higher popularity than the threshold
G = createPopularityThreshGraph (nodes_df, edges_df, popularityThreshold)



# Print the number of nodes and edges
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")


genre = "hip hop"
K = createGenreGraph (nodes_df, edges_df, genre)
# Print the number of nodes and edges
print(f"Number of nodes: {K.number_of_nodes()}")
print(f"Number of edges: {K.number_of_edges()}")

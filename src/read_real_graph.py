import pandas as pd
import os
import networkx as nx
import networkit as nk

def read_dataset():
    # Gets the current directory where the script is located
    current_dir = os.path.dirname(__file__)
    current_dir = current_dir.replace("src", "dataset")

    # Builds full paths to .csv files within the current directory
    nodes_path = os.path.join(current_dir, 'nodes.csv')
    edges_path = os.path.join(current_dir, 'edges.csv')

    # Upload CSV files using paths relative to the current directory, limited to a subset of rows
    nodes_df = pd.read_csv(nodes_path)#, nrows=1000)  #limite 1.000 nodi
    edges_df = pd.read_csv(edges_path)#, nrows=1000)  #limite 1.000 edges

    return nodes_df, edges_df

def get_size():
    
    current_dir = os.path.dirname(__file__)
    current_dir = current_dir.replace("src", "dataset")
    nodes_path = os.path.join(current_dir, 'nodes.csv')
    nodes_df = pd.read_csv(nodes_path)

    return len(nodes_df)

def create_graph_networkx():

    nodes_df, edges_df = read_dataset()

    # Create Graph
    G = nx.Graph()

    # Add nodes on the graph
    for _, row in nodes_df.iterrows():
        G.add_node(row['spotify_id'], name=row['name'], followers=row['followers'],
                popularity=row['popularity'], genres=row['genres'], chart_hits=row['chart_hits'])

    # Add edges on the graph (limited to the first 10,000 edges)
    for _, row in edges_df.iterrows():
        G.add_edge(row['id_0'], row['id_1'])

    return G

def create_graph_networkit():

    #nodes_df, edges_df = read_dataset()
    pass
import pandas as pd
import os
import networkx as nx
import networkit as nk

def read_dataset():
    """
    Reads file of real graph dataset and returns nodes and edges

    Returns:
        pandas dataframe containing nodes of real graph
        pandas dataframe containing edges of real graph
    """
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
    """
    Get size of real graph
    """
    current_dir = os.path.dirname(__file__)
    current_dir = current_dir.replace("src", "dataset")
    nodes_path = os.path.join(current_dir, 'nodes.csv')
    nodes_df = pd.read_csv(nodes_path)

    return len(nodes_df)

def create_graph_nx():
    """
    Create networkx representation of real graph

    Returns:
        networkx graph: representation of real graph
    """
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

def nx2nk(nx_graph):
    """
    Converts networkx graph into networkit graph
    """
    node_mapping = {node: i for i, node in enumerate(nx_graph.nodes())}
    # Initialize an empty networkit graph
    nk_graph = nk.graph.Graph(n=len(node_mapping), weighted=False)
    
    # Create a new attribute named 'nameAtt' of type 'str'
    global nameAtt
    nameAtt = nk_graph.attachNodeAttribute("name", str)

    for node in nx_graph.nodes():
        nameAtt[node_mapping[node]] = str(nx_graph.nodes[node].get('name', str(node)))


    # the commented code can create a graph suitable for the SILVAN algorithm
    #with open('graphMain.txt', 'w') as f:
        # Add edges from the NetworkX graph to the NetworKit graph
    for u, v, data in nx_graph.edges(data=True):
        weight = 1.0  # Default weight if unweighted
        nk_graph.addEdge(node_mapping[u], node_mapping[v], weight)
            #write to graph
            #f.write(f"{node_mapping[u]}  {node_mapping[v]}\n")


    return nk_graph
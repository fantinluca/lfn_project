import pandas as pd
import os, re
import networkx as nx
import networkit as nk
import numpy as np

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

# creates a subGraph only with the nodes of a certain genre
def create_genre_subgraph(nodes_df, edges_df, genre):
    """
    Creates a networkx graph with only the nodes correlated to a certain genre.
    The edges are only between nodes which satisfy the above-mentioned condition.

    Parameters:
        nodes of the original graph
        edges of the original graph
        genre(s)
    
    Returns:
        a networkx graph 
    """

    # Create Graph
    G = nx.Graph()

    # Add nodes on the graph
    for index, row in nodes_df.iterrows():
        # a node will be added only if it contains the genre
        regex_list = re.findall(r'\'(.*?)\'', row['genres'])
        # if it contains the genre
        if (any(genre in g for g in regex_list)):
            G.add_node(row['spotify_id'], name=row['name'], followers=row['followers'],
                popularity=row['popularity'], genres=row['genres'], chart_hits=row['chart_hits'])

    # Add edges on the graph
    for index, row in edges_df.iterrows():
        # add the edge only if both nodes are in the graph
        if ( row['id_0'] in G and row['id_1'] in G ):
            G.add_edge(row['id_0'], row['id_1'])

    return G


def create_popularity_subgraph (nodes_df, edges_df, popularity_threshold):
    """
    Creates a networkx graph with only the nodes correlated to artists with popularity greater than a threshold.
    The edges are only between nodes which satisfy the above-mentioned condition.

    Parameters:
        nodes of the original graph
        edges of the original graph
        popularity threshold

    Returns:
        a networkx graph 
    """

    # Create Graph
    G = nx.Graph()

    # Add nodes on the graph
    for index, row in nodes_df.iterrows():
        # a node will be added only if it's more popular than the threshold
        if (row['popularity'] >= popularity_threshold):
            G.add_node(row['spotify_id'], name=row['name'], followers=row['followers'],
                popularity=row['popularity'], genres=row['genres'], chart_hits=row['chart_hits'])

    # Add edges on the graph
    for index, row in edges_df.iterrows():
        # add the edge only if both nodes are in the graph
        if ( row['id_0'] in G and row['id_1'] in G ):
            G.add_edge(row['id_0'], row['id_1'])
    
    return G


def create_popularity_percent_subgraph (nodes_df, edges_df, percentage_threshold):
    """
    Creates a networkx graph with only the x% most popular nodes where x = percentage_threshold
    The edges are only between nodes which satisfy the above-mentioned condition.

    Parameters:
        nodes of the original graph
        edges of the original graph
        percentage threshold = number between 0 and 100

    Returns:
        a networkx graph 
    """
    # prima di tutto prendi tutti i valori di popolarità, ordinali e capisci qual è il threshold, 
    # poi richiama l'altro metodo con quel threshold

    # emtpy list
    values = []
    for index, row in nodes_df.iterrows():
        values.append(row['popularity'])

    # Step 3: Convert the list to a NumPy array
    my_array = np.array(values)

    # Calculate the percentile
    percent = 100 - percentage_threshold
    threshold = np.percentile(my_array, percent)

    return create_popularity_subgraph (nodes_df, edges_df, threshold)





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
import pandas as pd
import os
import networkx as nx
import networkit as nk



def convert_to_networkit(nx_graph):
    node_mapping = {node: i for i, node in enumerate(nx_graph.nodes())}
    # Initialize an empty networkit graph
    nk_graph = nk.graph.Graph(n=len(node_mapping), weighted=False)
    
    # Create a new attribute named 'nameAtt' of type 'str'
    global nameAtt
    nameAtt = nk_graph.attachNodeAttribute("name", str)

    for node in nx_graph.nodes():
        nameAtt[node_mapping[node]] = str(nx_graph.nodes[node].get('name', str(node)))

    # the commented code can create a graph suitable for the SILVAN algorithm
    #with open('subGraph.txt', 'w') as f:
    # Add edges from the NetworkX graph to the NetworKit graph
    for u, v, data in nx_graph.edges(data=True):
        weight = 1.0  # Default weight if unweighted
        nk_graph.addEdge(node_mapping[u], node_mapping[v], weight)
        #attName[node_mapping[u]] = G.nodes[u]['name']
        #f.write(f"{node_mapping[u]}  {node_mapping[v]}\n")

    return nk_graph





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
popularityThreshold = 70


# Create Graph
G = nx.Graph()

# Add nodes on the graph
for index, row in nodes_df.iterrows():
    # a node will be added only if it's more popular than the threshold
    if ( row['popularity'] > popularityThreshold  ):
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
    print(f"Node: {node}, Name: {data.get('name', 'No name attribute')}, Popularity = {data.get('popularity')}  Genres = {data.get('genres')}")


# -----------------------------------------------------------------------------------------------------------------------------------------
# Compute various measures  
print("\n\n\n\n")


# Centrality Measures and display top 10 nodes for each
# Degree Centrality
degree_centrality = nx.degree_centrality(G)
top_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Degree Centrality:")
for node, centrality in top_degree_centrality:
    print(f"Node: {node}, Name: { G.nodes[node]['name']  }, Degree Centrality: {centrality}")

# Closeness Centrality
closeness_centrality = nx.closeness_centrality(G)
top_closeness_centrality = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Closeness Centrality:")
for node, centrality in top_closeness_centrality:
    print(f"Node: {node}, Name: {G.nodes[node]['name']}, Closeness Centrality: {centrality}")

# Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G)
top_betweenness_centrality = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Betweenness Centrality:")
for node, centrality in top_betweenness_centrality:
    print(f"Node: {node}, Name: {G.nodes[node]['name']}, Betweenness Centrality: {centrality}")

# PageRank
pagerank = nx.pagerank(G) 
top_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 PageRank:")
for node, rank in top_pagerank:
    print(f"Node: {node}, Name: {G.nodes[node]['name']}, PageRank: {rank}")

# Eigenvector Centrality
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
top_eigenvector_centrality = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Eigenvector Centrality:")
for node, centrality in top_eigenvector_centrality:
    print(f"Node: {node}, Name: {G.nodes[node]['name']}, Eigenvector Centrality: {centrality}")




# LOCAL clustering coefficients
G_nk = convert_to_networkit(G)
print(nk.overview(G_nk))


#clustCoeff = nk.globals.ClusteringCoefficient.exactGlobal(G_nk)
clustCoeff = nk.centrality.LocalClusteringCoefficient(G_nk)                 # Local clustering coefficient
# Run the algorithm to compute the coefficients
clustCoeff.run()

# Retrieve the clustering coefficients for each node
clustering_coefficients = clustCoeff.scores()

# Print the coefficients for each node
#for node, coeff in enumerate(clustering_coefficients):
#    print(f"Node {node}: Clustering Coefficient = {coeff}")
top_clustCoeff = sorted(clustering_coefficients, key=lambda x: x, reverse=True)[:10]
list_top_coeff_pairs = list(enumerate(top_clustCoeff))
print("\nTop 10 Local clustering Coefficients:")
for node, coeff in enumerate(list_top_coeff_pairs):
    print(f"Node: {node}, Name: {nameAtt[node]}  , Clustering Coefficient = {coeff}")



# GLOBAL CLUSTERING COEFF
globClustCoeff = nk.globals.ClusteringCoefficient.exactGlobal(G_nk)
print ("Global cc = ", globClustCoeff )


# APPROX GLOBAL CLUSTERING COEFF
globClustCoeffApprox = nk.globals.ClusteringCoefficient.approxGlobal(G_nk, trials = 10000)
print ("Approx global cc = ", globClustCoeffApprox )


import pandas as pd
import os
import networkx as nx
import networkit as nk

from create_graphs import create_graph_networkit, create_graph_networkx


def convert_to_networkit(nx_graph):
    node_mapping = {node: i for i, node in enumerate(nx_graph.nodes())}
    # Initialize an empty networkit graph
    nk_graph = nk.graph.Graph(n=len(node_mapping), weighted=False)
    
    # Create a new attribute named 'nameAtt' of type 'str'
    global nameAtt
    nameAtt = nk_graph.attachNodeAttribute("name", str)



    for node in nx_graph.nodes():
        nameAtt[node_mapping[node]] = str(nx_graph.nodes[node].get('name', str(node)))


    #with open('graphMain.txt', 'w') as f:
        # Add edges from the NetworkX graph to the NetworKit graph
    for u, v, data in nx_graph.edges(data=True):
        weight = 1.0  # Default weight if unweighted
        nk_graph.addEdge(node_mapping[u], node_mapping[v], weight)
            #write to graph
            #f.write(f"{node_mapping[u]}  {node_mapping[v]}\n")


    return nk_graph


G = create_graph_networkx()

# Centrality Measures and display top 10 nodes for each
# Degree Centrality
degree_centrality = nx.degree_centrality(G)
top_degree_centrality = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Degree Centrality:")
for node, centrality in top_degree_centrality:
    print(f"Node: {node},  Name: { G.nodes[node]['name']  },  Degree Centrality: {centrality}")
'''
# Closeness Centrality
closeness_centrality = nx.closeness_centrality(G)
top_closeness_centrality = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Closeness Centrality:")
for node, centrality in top_closeness_centrality:
    print(f"Node: {node},   Name: { G.nodes[node]['name']  },  Closeness Centrality: {centrality}")

# Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G)
top_betweenness_centrality = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Betweenness Centrality:")
for node, centrality in top_betweenness_centrality:
    print(f"Node: {node},   Name: { G.nodes[node]['name']  },  Betweenness Centrality: {centrality}")

# PageRank
pagerank = nx.pagerank(G) 
top_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 PageRank:")
for node, rank in top_pagerank:
    print(f"Node: {node},   Name: { G.nodes[node]['name']  },  PageRank: {rank}")

# Eigenvector Centrality
eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
top_eigenvector_centrality = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("\nTop 10 Eigenvector Centrality:")
for node, centrality in top_eigenvector_centrality:
    print(f"Node: {node},   Name: { G.nodes[node]['name']  },  Eigenvector Centrality: {centrality}")
'''



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
    print(f"Node: {node}, Name: {nameAtt[node]},  Clustering Coefficient = {coeff}")


# GLOBAL CLUSTERING COEFF
globClustCoeff = nk.globals.ClusteringCoefficient.exactGlobal(G_nk)
print ("Global cc = ", globClustCoeff )


# APPROX GLOBAL CLUSTERING COEFF
globClustCoeffApprox = nk.globals.ClusteringCoefficient.approxGlobal(G_nk, trials = 10000)
print ("Approx global cc = ", globClustCoeffApprox )



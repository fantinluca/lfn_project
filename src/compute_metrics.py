import networkx as nx
import networkit as nk
from time import time
from create_graphs import nx2nk

# metrics: list
def compute_all_metrics(nx_graph):

    node_metrics = {
        "node": [],
        "degree_centrality": [], 
        "closeness_centrality": [],
        "betweenness_centrality": [],
        "pagerank_centrality": [],
        "eigenvector_centrality": [],
        "clustering_coefficient": [],
    }

    connected_components = list(nx.connected_components(nx_graph))
    num_connected_components = len(connected_components)
    print(f"Number of connected components computed")

    # --- Calculate Average Clustering Coefficient ---
    avg_clustering_coefficient = nx.average_clustering(nx_graph)
    print(f"Average clustering coefficient computed")

    # --- Calculate Centrality Metrics ---
    # Degree Centrality
    degree_centrality = nx.degree_centrality(nx_graph)
    print(f"Degree centralities calculated.")

    # Closeness Centrality
    closeness_centrality = nx.closeness_centrality(nx_graph)
    print(f"Closeness centralities calculated.")

    # Betweenness Centrality
    betweenness_centrality = nx.betweenness_centrality(nx_graph)
    print(f"Betweenness centralities calculated.")

    # PageRank
    pagerank_centrality = nx.pagerank(nx_graph)
    print(f"PageRank centralities calculated.")

    # Eigenvector Centrality
    eigenvector_centrality = nx.eigenvector_centrality(nx_graph, max_iter=1000, tol=1e-06)
    print(f"Eigenvector centralities calculated.")

    nk_graph = nx2nk(nx_graph)

    # Local clustering coefficient
    clust_coeff = nk.centrality.LocalClusteringCoefficient(nk_graph)
    clust_coeff.run()
    clustering_coefficients = clust_coeff.scores()

    # global clustering coefficient
    global_clustering_coefficient = nk.globals.ClusteringCoefficient.exactGlobal(nk_graph)

    # approximate clustering coefficient
    global_clustering_coefficient_approx = nk.globals.ClusteringCoefficient.approxGlobal(nk_graph, trials = 10000)

    # --- Collect Metrics ---
    nodes = nx_graph.nodes()
    for i in range(len(nodes)):
        node = list(nodes)[i]
        node_metrics["node"].append(node)
        node_metrics["degree_centrality"].append(degree_centrality.get(node, 0))
        node_metrics["closeness_centrality"].append(closeness_centrality.get(node, 0))
        node_metrics["betweenness_centrality"].append(betweenness_centrality.get(node, 0))
        node_metrics["pagerank_centrality"].append(pagerank_centrality.get(node, 0))
        node_metrics["eigenvector_centrality"].append(eigenvector_centrality.get(node, 0))
        node_metrics["clustering_coefficient"].append(clustering_coefficients[i])

    graph_metrics = {
        "num_connected_components": num_connected_components,
        "avg_clustering_coefficient": avg_clustering_coefficient,
        "global_clustering_coefficient": global_clustering_coefficient,
        "global_clustering_coefficient_approx": global_clustering_coefficient_approx
    }

    return graph_metrics, node_metrics
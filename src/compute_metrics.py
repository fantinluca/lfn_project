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

    starting_time = time()
    connected_components = list(nx.connected_components(nx_graph))
    num_connected_components = len(connected_components)
    print(f"Number of connected components computed in {time()-starting_time} seconds")

    # --- Calculate Average Clustering Coefficient ---
    starting_time = time()
    avg_clustering_coefficient = nx.average_clustering(nx_graph)
    print(f"Average clustering coefficient computed in {time()-starting_time} seconds")

    # --- Calculate Centrality Metrics ---
    # Degree Centrality
    starting_time = time()
    degree_centrality = nx.degree_centrality(nx_graph)
    print(f"Degree centralities computed in {time()-starting_time} seconds")

    # Closeness Centrality
    starting_time = time()
    closeness_centrality = nx.closeness_centrality(nx_graph)
    print(f"Closeness centralities computed in {time()-starting_time} seconds")

    # Betweenness Centrality
    starting_time = time()
    betweenness_centrality = nx.betweenness_centrality(nx_graph)
    print(f"Betweenness centralities computed in {time()-starting_time} seconds")

    # PageRank
    starting_time = time()
    pagerank_centrality = nx.pagerank(nx_graph)
    print(f"PageRank centralities computed in {time()-starting_time} seconds")

    # Eigenvector Centrality
    starting_time = time()
    eigenvector_centrality = nx.eigenvector_centrality(nx_graph, max_iter=1000, tol=1e-06)
    print(f"Eigenvector centralities computed in {time()-starting_time} seconds")

    nk_graph = nx2nk(nx_graph)

    # Local clustering coefficient
    starting_time = time()
    clust_coeff = nk.centrality.LocalClusteringCoefficient(nk_graph)
    clust_coeff.run()
    clustering_coefficients = clust_coeff.scores()
    print(f"Clustering coefficients computed in {time()-starting_time} seconds")

    # global clustering coefficient
    starting_time = time()
    global_clustering_coefficient = nk.globals.ClusteringCoefficient.exactGlobal(nk_graph)
    print(f"Global clustering coefficient computed in {time()-starting_time} seconds")

    # approximate clustering coefficient
    starting_time = time()
    global_clustering_coefficient_approx = nk.globals.ClusteringCoefficient.approxGlobal(nk_graph, trials = 10000)
    print(f"Approximate global clustering coefficient computed in {time()-starting_time} seconds")

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
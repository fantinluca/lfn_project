import networkx as nx
import networkit as nk
from constants import METRICS
from time import time
from create_graphs import nx2nk

# metrics: list
def compute_metrics(nx_graph, metric_list):
    graph_metrics = {}
    node_metrics = {"node": nx_graph.nodes()}

    for metric in metric_list:
        result = globals()[metric](nx_graph)
        if type(result) is list: # is a node-level metric
            node_metrics[metric] = result
        elif type(result) is dict:
            node_metrics[metric] = list(result.values())
        else: # is a graph-level metric
            graph_metrics[metric] = result

    return graph_metrics, node_metrics

def connected_components(nx_graph):
    connected_components = list(nx.connected_components(nx_graph))
    return len(connected_components)

def avg_clustering_coeff(nx_graph):
    return nx.average_clustering(nx_graph)

def global_clustering_coeff(nx_graph):
    nk_graph = nx2nk(nx_graph)
    return nk.globals.ClusteringCoefficient.exactGlobal(nk_graph)

def approx_global_clustering_coeff(nx_graph):
    nk_graph = nx2nk(nx_graph)
    return nk.globals.ClusteringCoefficient.approxGlobal(nk_graph, trials = 10000)

def degree(nx_graph):
    return nx.degree_centrality(nx_graph)

def closeness(nx_graph):
    return nx.closeness_centrality(nx_graph)

def betweenness(nx_graph):
    return nx.betweenness_centrality(nx_graph)

def pagerank(nx_graph):
    return nx.pagerank(nx_graph)

def eigenvector(nx_graph):
    return nx.eigenvector_centrality(nx_graph, max_iter=1000, tol=1e-06)

def clustering_coeffs(nx_graph):
    nk_graph = nx2nk(nx_graph)
    clust_coeff = nk.centrality.LocalClusteringCoefficient(nk_graph)
    clust_coeff.run()
    return clust_coeff.scores()
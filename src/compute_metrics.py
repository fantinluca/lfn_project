import networkx as nx
import networkit as nk

import utils
from create_graphs import nx2nk

# metrics: list
def compute_metrics(nx_graph, metric_list):
    """
    Computes desired metrics for input graph

    Args:
        nx_graph (networkx graph): input graph
        metric_list (list of strings): names of the metrics to compute for nx_graph

    Returns:
        dict string->float: graph metrics computed for nx_graph
        dict string->list of floats: node metrics computed for nx_graph, contains list of nodes and lists with metric values
    """
    graph_metrics = {"n_nodes": nx_graph.number_of_nodes(), "n_edges": nx_graph.number_of_edges()}
    node_metrics = {"node": nx_graph.nodes()}

    # compute graph level metrics
    for m in utils.METRICS[:utils.SEP_ID]:
        if m in metric_list:
            result = globals()[m](nx_graph)
            graph_metrics[m] = result

    # compute node level metrics
    for m in utils.METRICS[utils.SEP_ID:]:
        matches = [metric for metric in metric_list if m in metric]
        if len(matches)>0:
            result = globals()[m](nx_graph)
            if type(result) is dict: result = list(result.values())
            if matches == [m]: # compute only entire metric
                node_metrics[m] = result
            else: # compute only certain statistic of metric
                for match in matches:
                    mod = match.split("_", maxsplit=1)[0]
                    graph_metrics[match] = utils.NODE_METRIC_MODIFIERS[mod](result)

    return graph_metrics, node_metrics

def connected_components(nx_graph):
    """
    Returns number of connected components of input graph
    """
    connected_components = list(nx.connected_components(nx_graph))
    return len(connected_components)

def avg_clustering_coeff(nx_graph):
    """
    Returns average global clustering coefficient of input graph
    """
    return nx.average_clustering(nx_graph)

def global_clustering_coeff(nx_graph):
    """
    Returns global clustering coefficient of input graph
    """
    nk_graph = nx2nk(nx_graph)
    return nk.globals.ClusteringCoefficient.exactGlobal(nk_graph)

def approx_global_clustering_coeff(nx_graph):
    """
    Returns global clustering coefficient of input graph computed with approximate method
    """
    nk_graph = nx2nk(nx_graph)
    return nk.globals.ClusteringCoefficient.approxGlobal(nk_graph, trials = 10000)

def degree(nx_graph):
    """
    Returns degree centrality for each node in input graph
    """
    return nx.degree_centrality(nx_graph)

def closeness(nx_graph):
    """
    Returns closeness centrality for each node in input graph
    """
    return nx.closeness_centrality(nx_graph)

def betweenness(nx_graph):
    """
    Returns betweenness centrality for each node in input graph
    """
    return nx.betweenness_centrality(nx_graph)

def pagerank(nx_graph):
    """
    Returns PageRank centrality for each node in input graph
    """
    return nx.pagerank(nx_graph)

def eigenvector(nx_graph):
    """
    Returns eigenvector centrality for each node in input graph
    """
    return nx.eigenvector_centrality(nx_graph, max_iter=1000, tol=1e-06)

def clustering_coeffs(nx_graph):
    """
    Returns clustering coefficient forr each node in input graph
    """
    nk_graph = nx2nk(nx_graph)
    clust_coeff = nk.centrality.LocalClusteringCoefficient(nk_graph)
    clust_coeff.run()
    return clust_coeff.scores()
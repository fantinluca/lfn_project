import os, argparse
import pandas as pd
import networkx as nx
from time import time

import create_graphs, compute_metrics, utils

# parse cmd arguments
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--metrics', nargs='*', default=utils.METRICS, choices=utils.METRICS)
parser.add_argument('--real', action='store_true')
parser.add_argument('--random', nargs='*', action=utils.RandomGraphAction)
parser.add_argument('--subgraph', nargs='*', action=utils.SubgraphsAction)
args = parser.parse_args()

# get results folder
if os.name == "posix":
    result_dir = os.path.join(os.getcwd(), "lfn_project", "results")
else:
    result_dir = os.path.dirname(__file__)
    result_dir = result_dir.replace("src", "results")

# create graphs according to cmd args
G = {}
real = args.real
random = args.random
subgraphs = args.subgraph
graph_types = []
if real:
    G["real"] = create_graphs.create_graph_nx()
    graph_types.append("real")
    print("Real graph created from dataset")
if random is not None:
    random_graphs_num = random["r"]
    for i in range(random_graphs_num):
        seed = int(str(time()).replace(".",""))
        G[f"rand_{'_'.join([str(e) for e in random.values()])}_{seed}_{i}"] = nx.powerlaw_cluster_graph(random["n"], random["m"], random["p"], seed=seed)
    graph_types.append('_'.join([str(e) for e in random.values()]))
    print(f"Created {random_graphs_num} random graphs with parameters n={random['n']}, m={random['m']}, p={random['p']} and label \'{random['label']}\'")
if subgraphs is not None:
    nodes, edges = create_graphs.read_dataset()
    if utils.SUBGRAPH_TYPES[0] in subgraphs.keys():
        genres = [s.lower() for s in subgraphs[utils.SUBGRAPH_TYPES[0]]]
        graph_types.append(f"sub_genres_{'_'.join(genres)}")
        for genre in genres:
            G[f"sub_genre_{genre}"] = create_graphs.create_genre_subgraph(nodes, edges, genre)
            print(f"Created subgraph of real graph containing only artists from genre {genre}")
    if utils.SUBGRAPH_TYPES[1] in subgraphs.keys():
        threshold = subgraphs[utils.SUBGRAPH_TYPES[1]]
        graph_types.append(f"sub_popularity_{threshold}")
        if type(threshold) is int:
            graph = create_graphs.create_popularity_subgraph(nodes, edges, threshold)
        else: # float
            graph = create_graphs.create_popularity_percent_subgraph(nodes, edges, threshold)
        G[f"sub_popularity_{threshold}"] = graph
        print(f"Created subgraph of real graph containing using popularity threhsold {threshold}")

# compute metrics for graph
G_metrics = {}
for name, graph in G.items():
    graph_metrics, node_metrics = compute_metrics.compute_metrics(graph, args.metrics)
    print(f"Computed metrics for graph {name}")
    G_metrics[name] = (graph_metrics, node_metrics)

# save/display metrics
for name, (graph_metrics, node_metrics) in G_metrics.items():

    if (len(node_metrics.keys()) > 1):
        metrics_df = pd.DataFrame(node_metrics)
        filename = f"{name}_node_metrics_{'_'.join(list(node_metrics.keys())[1:])}.csv"
        output_file = os.path.join(result_dir, filename)
        metrics_df.to_csv(output_file, sep=";", index=False)
        print(f"All metrics for graph {name} saved to {output_file}.")

    if (len(graph_metrics.keys()) > 0):
        print(f"Graph-level metrics for graph {name}:")
        for name, value in graph_metrics.items():
            print(f"{name}: {value}")
        
# save graph metrics in csv
graph_names = list(G_metrics.keys())
graph_level_metrics = [metrics[0] for metrics in G_metrics.values()] # tutti dict
glm_df = pd.DataFrame(graph_level_metrics)
glm_df["graph"] = graph_names
glm_df = glm_df.set_index("graph")
filename = f"{'-'.join(graph_types)}_graph_metrics.csv"
output_file = os.path.join(result_dir, filename)
glm_df.to_csv(output_file, sep=";", index=True)
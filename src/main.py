import os, argparse
import pandas as pd
import networkx as nx
from time import time

import create_graphs, compute_metrics, constants

# parse cmd arguments
parser = argparse.ArgumentParser()
parser.add_argument('-m', '--metrics', nargs='*', default=constants.METRICS, choices=constants.METRICS)
parser.add_argument('-g', '--graph', nargs='*')
#parser.add_argument('-s', '--subgraphs', nargs='*')
args = parser.parse_args()

# get results folder
result_dir = os.path.dirname(__file__)
result_dir = result_dir.replace("src", "results")

# create graph according to cmd args
graph_args = args.graph
graph_type = graph_args[0]
if graph_type == "real":
    G = {"real": create_graphs.create_graph_nx()}
elif graph_type == "random":
    random_graphs_num = int(graph_args[1])
    seed = int(str(time()).replace(".",""))
    G = {f"rand_{seed}":nx.powerlaw_cluster_graph(constants.n, constants.m, constants.p, seed=seed) for _ in range(random_graphs_num)}

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
        if graph_type == "real": filename = f"real_node_metrics_{'_'.join(list(node_metrics.keys())[1:])}.csv"
        else: filename = os.path.join(result_dir, f"{name}_node_metrics.csv")
        output_file = os.path.join(result_dir, filename)
        metrics_df.to_csv(output_file, sep=";", index=False)
        print(f"All metrics for graph {name} saved to {output_file}.")

    if (len(graph_metrics.keys()) > 0):
        print(f"Graph-level metrics for graph {name}:")
        for name, value in graph_metrics.items():
            print(f"{name}: {value}")
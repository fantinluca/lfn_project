import os
import pandas as pd
import networkx as nx
import itertools as it
from time import time

import create_graphs, compute_metrics, utils

# get results folder
if os.name == "posix":
    result_dir = os.path.join(os.getcwd(), "lfn_project", "results")
else:
    result_dir = os.path.dirname(__file__)
    result_dir = result_dir.replace("src", "results")

G = create_graphs.create_graph_nx()

nodes_df, _ = create_graphs.read_dataset()
nodes_df = nodes_df.rename(columns={"spotify_id": "node"})
nodes_df = nodes_df.set_index("node")

df = pd.read_csv("../results/real_node_metrics_clustering_coeffs.csv", sep=';', index_col=0)
df = df.join(nodes_df["name"], lsuffix="_metrics", rsuffix="_dataset")
df = df.sort_values("clustering_coeffs", ascending=False)

cc1 = df.index[df["clustering_coeffs"]==1.0].to_list()
not_verified_count = 0
for node in cc1:
    #if node!="6vCU4ORbNFUSNXe7mnsbWX": continue
    hp_verified = True
    con_comp = nx.node_connected_component(G, node)
    for node_pair in it.combinations(con_comp, 2):
        if not (G.has_edge(node, node_pair[0]) and G.has_edge(node, node_pair[1]) and G.has_edge(node_pair[0], node_pair[1])):
            hp_verified = False
            break
    
    if not hp_verified: not_verified_count += 1
    print(f"Hypothesis {'not' if not hp_verified else ''} verified for artist {df.loc[node]['name']}")
    break

print(f"In the end, hypothesis not verified for {not_verified_count} artists out of {len(cc1)} artists")
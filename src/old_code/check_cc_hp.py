import os
import pandas as pd
import networkx as nx
import itertools as it

import create_graphs

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

df = pd.read_csv(os.path.join(result_dir, "real", "real_node_metrics_clustering_coeffs.csv"), sep=';', index_col=0)
df = df.join(nodes_df["name"], lsuffix="_metrics", rsuffix="_dataset")
df = df.sort_values("clustering_coeffs", ascending=False)

cc1 = df.index[df["clustering_coeffs"]==1.0].to_list()
not_verified_count = 0
for node in cc1:
    hp_verified = True
    neigh = nx.neighbors(G, node)
    for node_pair in it.combinations(neigh, 2):
        if not G.has_edge(node_pair[0], node_pair[1]):
            not_verified_count += 1
            print(f"Hypothesis not verified for artist {df.loc[node]['name']}")

print(f"In the end, hypothesis not verified for {not_verified_count} artists out of {len(cc1)} artists")
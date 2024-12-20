import pandas as pd
import os

import create_graphs, compute_metrics

# create real graph
G = create_graphs.create_graph_nx()

result_dir = os.path.dirname(__file__)
result_dir = result_dir.replace("src", "results")

# compute metrics for graph
graph_metrics, node_metrics = compute_metrics.compute_all_metrics(G)
print("Computed metrics for graph")

# save node metrics to csv
metrics_df = pd.DataFrame(node_metrics)
output_file = os.path.join(result_dir, "real_graph_node_metrics.csv")
metrics_df.to_csv(output_file, sep=";", index=False)
print(f"All metrics for real graph saved to {output_file}.")

# save graph metrics to csv file
print("Graph-level metrics:")
for name, value in graph_metrics.items():
    print(f"{name}: {value}")
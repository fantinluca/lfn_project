# list of available metrics
METRICS = [
    "connected_components",
    "avg_clustering_coeff",
    "global_clustering_coeff",
    "approx_global_clustering_coeff",
    "degree",
    "closeness",
    "betweenness",
    "pagerank",
    "eigenvector",
    "clustering_coeffs"
]

# Parameters for the Power Law Clustered Graph
n = 10 # Number of nodes (1/50 of the real graph)
m = 2  # Number of edges to add for each new node
p = 0.3  # Clustering probability
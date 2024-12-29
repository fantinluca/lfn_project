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
"""List of available metrics"""

# Parameters for the Power Law Clustered Graph
n = 10
""" Default number of nodes for Power Law Clustered Graph """
m = 2
""" Default number of edges to add for each new node for Power Law Clustered Graph """
p = 0.3 
""" Default clustering probability for Power Law Clustered Graph """
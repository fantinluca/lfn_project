import argparse
import utils
from statistics import mean

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

NODE_METRIC_MODIFIERS = {
    "max": max,
    "avg": mean
}
"""Dictionaries of available modifiers for node level metrics as keys and corresponding methods as values"""

SEP_ID = 4
"""Index of the first node level metric in METRICS"""

# Parameters for the Power Law Clustered Graph
r = 1
""" Default number of random graphs to generate """
n = 10
""" Default number of nodes for Power Law Clustered Graph """
m = 2
""" Default number of edges to add for each new node for Power Law Clustered Graph """
p = 0.3 
""" Default clustering probability for Power Law Clustered Graph """

SUBGRAPH_TYPES = [
    "genre",
    "popularity"
]
""" Available types of subgraphs """

class RandomGraphAction(argparse.Action):
    """
    Class specifying how the cmd arguments for random graphs are processed
    """
    def __call__(self, parser, namespace, values, option_string = None):
        if len(values)>5:
            raise argparse.ArgumentTypeError(f"Argument {self.dest} does not accept more than 4 values")
        complete_values = {}
        i = 0
        complete_values["label"] = values[i] if len(values)>i else ''
        i += 1
        complete_values["r"] = int(values[i]) if len(values)>i else r
        i += 1
        complete_values["n"] = int(values[i]) if len(values)>i else n
        i += 1
        complete_values["m"] = int(values[i]) if len(values)>i else m
        i += 1
        complete_values["p"] = float(values[i]) if len(values)>i else p
        setattr(namespace, self.dest, complete_values)

class SubgraphsAction(argparse.Action):
    """
    Class specifying how the cmd arguments for subgraphs are processed
    """
    def __call__(self, parser, namespace, values, option_string = None):
        no_type=0
        genre_ind=-1
        popularity_ind=-1
        complete_values = {}

        # check if at least one subgraph type is specified

        try:
            genre_ind = values.index(utils.SUBGRAPH_TYPES[0])
        except ValueError:
            no_type -= 1
        try:
            popularity_ind = values.index(utils.SUBGRAPH_TYPES[1])
        except ValueError:
            no_type -= 1
        if no_type==-2: raise argparse.ArgumentTypeError(f"No subgraph type specified among {', '.join(utils.SUBGRAPH_TYPES)}")
        
        # store genres
        if genre_ind!=-1:
            end_index = popularity_ind if genre_ind<popularity_ind else len(values)
            genres = values[genre_ind+1:end_index]
            complete_values[utils.SUBGRAPH_TYPES[0]] = genres

        # store popularity threshold
        if popularity_ind!=-1:
            try:
                threshold = float(values[popularity_ind+1])
                if threshold>0 or threshold<1: # percentage threshold
                    complete_values[utils.SUBGRAPH_TYPES[1]] = threshold
                elif (threshold>0 or threshold<100) and threshold.is_integer():
                    complete_values[utils.SUBGRAPH_TYPES[1]] = int(threshold)
                else:
                    raise argparse.ArgumentTypeError("Popularity threshold must be either an integer between 0 and 100 or a float between 0 and 1")
            except IndexError: raise argparse.ArgumentTypeError("No threshold specified for popularity subgraph")
            except ValueError: raise argparse.ArgumentTypeError("Invalid value for popularity threshold entered")

        setattr(namespace, self.dest, complete_values)
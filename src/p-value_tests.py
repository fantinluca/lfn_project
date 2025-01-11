import pandas as pd
import os, scipy, statistics, utils

alpha = 0.05

result_dir = os.path.dirname(__file__)
result_dir = result_dir.replace("src", "results")
result_dir = os.path.join(result_dir, "rand")

rand_dir = os.path.join(result_dir, "rand")
real_dir = os.path.join(result_dir, "real")
genre_dir = os.path.join(result_dir, "sub_genre")

#rand_file = os.path.join(result_dir, "rand_random_house_100_3249_3_0.6_graph_metrics.csv")
#df = pd.read_csv(rand_file, sep=';', index_col=0)
#values = df["max_eigenvector"].to_list()

rand_files = {f.split("_")[2]: os.path.join(rand_df, f) for f in os.listdir(rand_dir) if f.startswith("rand")}

for random_graph, file in rand_files.items():
    rand_df = pd.read_csv(file, sep=';', index_col=0)
    results = {}

    metrics = list(rand_df.columns)[2:]
    if "connected_components" in metrics: metrics.remove("connected_components")

    # get value to be compared
    for metric in metrics:
        graph_level = not any(m in metric for m in ["closeness", "eigenvector"])

        values_to_compare = {}
        if random_graph=="real":
            if graph_level: filename = "real_graph_metrics.csv"
            else: filename = f"real_node_metrics_{metric}.csv"
            file_df = pd.read_csv(os.path.join(real_dir, filename), sep=";", index_col=0)
            if graph_level: values_to_compare[metric] = file_df.loc["real"][metric]
            else:
                mod, m = metric.split("_", maxsplit=1)
                values_to_compare[metric] = utils.NODE_METRIC_MODIFIERS[mod](file_df[m])
        else: # genere
            if graph_level: filename = "real_graph_metrics.csv"
            else: filename = f"real_node_metrics_{metric}.csv"
            file_df = pd.read_csv(os.path.join(real_dir, filename), sep=";", index_col=0)
            if graph_level: values_to_compare[metric] = file_df.loc["real"][metric]
            else:
                mod, m = metric.split("_", maxsplit=1)
                values_to_compare[metric] = utils.NODE_METRIC_MODIFIERS[mod](file_df[m])

    for metric in metrics:
        data = rand_df[metric].to_list()

#prob = scipy.stats.norm.pdf(1.246736e-01, loc=statistics.mean(values), scale=statistics.stdev(values))
#print(prob)

"""
parser = argparse.ArgumentParser()
parser.add_argument("-r", "--random", nargs='*', default="all")
parser.add_argument('-m', '--metrics', nargs='*', default="all")
args = parser.parse_args()

alpha = 0.05

result_dir = os.path.dirname(__file__)
result_dir = result_dir.replace("src", "results")
result_dir = os.path.join(result_dir, "rand")

rand_files = {f.split("_")[2]: os.path.join(result_dir, f) for f in os.listdir(result_dir) if f.startswith("rand")}

for random_graph, file in rand_files.items():
    df = pd.read_csv(file, sep=';', index_col=0)
    results = {}
    
    metrics = list(df.columns)[2:]
    if "connected_components" in metrics: metrics.remove("connected_components")

    for metric in metrics:
        data = df[metric].to_list()

        # plot histogram of data
        plt.clf()
        plt.hist(data)
        plt.title(f"{random_graph}; {metric}")
        plt.savefig(os.path.join(result_dir, "dist_plots", f"dist_plot_{random_graph}_{metric}.png"))

        stat, p = shapiro(data)
        results[metric] = (stat, p, f"Probably {'not ' if p>alpha else ''}Gaussian")

    result_df = pd.DataFrame.from_dict(results, orient='index')
    result_df.index.name = "metric"
    result_df.columns = ["statistic", "p-value", "output"]
    result_df.to_csv(os.path.join(result_dir, "normality_tests", f"normality_test_{random_graph}.csv"), sep=";")
"""
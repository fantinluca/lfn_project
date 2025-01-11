from scipy.stats import shapiro
import pandas as pd
import matplotlib.pyplot as plt
import os

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
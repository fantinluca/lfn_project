from scipy.stats import shapiro
import pandas as pd
import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--random", nargs='*', default="all")
parser.add_argument('-m', '--metrics', nargs='*', default="all")
args = parser.parse_args()

alpha = 0.05

result_dir = os.path.dirname(__file__)
result_dir = result_dir.replace("src", "results")
result_dir = os.path.join(result_dir, "rand")

if args.random=="all":
    rand_files = {f.split("_")[2]: f for f in os.listdir(result_dir)}
else:
    rand_files = {rg: f for f in os.listdir(result_dir) for rg in args.random if rg in f}
rand_files = {rg: os.path.join(result_dir, f) for rg, f in rand_files.items()}

for random_graph, file in rand_files.items():
    df = pd.read_csv(file, sep=';', index_col=0)
    results = {}
    
    if args.metrics=="all":
        metrics = list(df.columns)[2:]
        if "connected_components" in metrics: metrics.remove("connected_components")
    else: metrics = args.metrics
    for metric in metrics:
        data = df[metric].to_list()
        stat, p = shapiro(data)
        results[metric] = (stat, p, f"Probably {'not ' if p>alpha else ''}Gaussian")

    result_df = pd.DataFrame.from_dict(results, orient='index')
    result_df.index.name = "metric"
    result_df.columns = ["statistic", "p-value", "output"]
    result_df.to_csv(os.path.join(result_dir, f"normality_test_{random_graph}.csv"), sep=";")
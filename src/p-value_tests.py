import pandas as pd
import os, scipy, statistics, utils

alpha = 0.05

result_dir = os.path.dirname(__file__)
result_dir = result_dir.replace("src", "results")

rand_dir = os.path.join(result_dir, "rand")
real_dir = os.path.join(result_dir, "real")
genre_dir = os.path.join(result_dir, "sub_genre")
popularity_dir = os.path.join(result_dir, "sub_popularity")

rand_files = {f.split("_")[2]: os.path.join(rand_dir, f) for f in os.listdir(rand_dir) if f.startswith("rand")}

for random_graph, file in rand_files.items():
    rand_df = pd.read_csv(file, sep=';', index_col=0)

    metrics = list(rand_df.columns)[2:]
    if "connected_components" in metrics: metrics.remove("connected_components")

    # get values to be compared
    values_to_compare = {}
    for metric in metrics:
        graph_level = not any(m in metric for m in ["closeness", "eigenvector"])
        mod = ""
        m = ""
        if not graph_level: mod, m = metric.split("_", maxsplit=1)

        if random_graph=="real":
            if graph_level: filename = "real_graph_metrics.csv"
            else: filename = f"real_node_metrics_{m}.csv"
            file_df = pd.read_csv(os.path.join(real_dir, filename), sep=";", index_col=0)
            if graph_level: values_to_compare[metric] = file_df.loc["real"][metric]
            else: values_to_compare[metric] = utils.NODE_METRIC_MODIFIERS[mod](file_df[m])
        elif random_graph=="top10popularity":
            if graph_level: filename = "sub_popularity_0.1_graph_metrics.csv"
            else: filename = "sub_popularity_0.1_node_metrics_betweenness_degree_closeness_pagerank_eigenvector_clustering_coeffs.csv"
            file_df = pd.read_csv(os.path.join(popularity_dir, filename), sep=";", index_col=0)
            if graph_level: values_to_compare[metric] = file_df.loc["sub_popularity_0.1"][metric]
            else: values_to_compare[metric] = utils.NODE_METRIC_MODIFIERS[mod](file_df[m])
        else: # genere
            if graph_level: filename = "graph_metrics_sub_genre.csv"
            else: filename = [f for f in os.listdir(genre_dir) if random_graph in f.split("_")][0]
            file_df = pd.read_csv(os.path.join(genre_dir, filename), sep=";", index_col=0)
            if graph_level: values_to_compare[metric] = file_df.loc[metric][random_graph]
            else: values_to_compare[metric] = utils.NODE_METRIC_MODIFIERS[mod](file_df[m])

    result_df = pd.DataFrame(columns=["output","prob_higher","prob_lower","subject","mean","stdev"])
    result_df.index.name = "metric"
    for metric in metrics:
        data = rand_df[metric].to_list()
        subject = values_to_compare[metric]
        mean = statistics.mean(data)
        std = statistics.stdev(data)
        prob_lower = scipy.stats.norm.cdf(subject, loc=mean, scale=std)
        output = "lower" if prob_lower > alpha else "higher" if 1-prob_lower > alpha else "equal"
        #print(f"Pr[X<={subject} | mean={mean}, stdev={std}] = {prob_lower}")
        result_df.loc[metric] = [output,1-prob_lower,prob_lower,subject,mean,std]
    result_df.to_csv(os.path.join(rand_dir, "p-value_tests", f"p-value_results_{random_graph}.csv"), sep=";")
import pandas as pd
import os
import re


# Gets the current directory where the script is located
current_dir = os.path.dirname(__file__)
current_dir = current_dir.replace("src", "dataset")

# Builds full paths to .csv files within the current directory
nodes_path = os.path.join(current_dir, 'nodes.csv')
edges_path = os.path.join(current_dir, 'edges.csv')

# Upload CSV files using paths relative to the current directory, limited to a subset of rows
nodes_df = pd.read_csv(nodes_path)
edges_df = pd.read_csv(edges_path)


# Create dictionary
genresDict = {}


''''
# Add nodes on the graph
for index, row in nodes_df.iloc[:10].iterrows():
    # Increment the value safely, adding the key if it doesn't exist
    #for genre in row['genres']:
    print(row['genres'])
    regexList = re.findall(r'\'(.*?)\'', row['genres'])
    for item in regexList:
        dict[item] = dict.get(item, 0) + 1
        print(item)
    print("\n")

print ("\n\n")
'''

# for every artist I look at all his genres
for index, row in nodes_df.iterrows():
    regexList = re.findall(r'\'(.*?)\'', row['genres'])
    for item in regexList:
        genresDict[item] = genresDict.get(item, 0) + 1



# Sorting the dictionary by value in descending order
sorted_dict = dict(sorted(genresDict.items(), key=lambda item: item[1], reverse=True))
#print the dictionary
print(sorted_dict)
#for key, value in sorted_dict.items():
#    print(f"{key}  ---  {value}")



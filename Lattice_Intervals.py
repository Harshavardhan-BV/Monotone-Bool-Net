#%%
import os
import numpy as np
import pandas as pd
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
from common_func import read_IO
from scipy.spatial.distance import pdist, squareform
plt.rcParams['svg.hashsalt'] = ''
os.makedirs('./figures/Intervals/',exist_ok=True)
#%%
n = 2
#%%
df = read_IO(n+1)
#%%
U = np.argmax(df,axis=1)
L = df.shape[1] - 1 - np.argmin(df.iloc[:, ::-1].values, axis=1)
# %%
# Calculate Hamming distances between all pairs of columns and choose only those 1 away
adj_mat = squareform(pdist(df.T, metric='hamming'))
adj_mat = (adj_mat == 1/len(df))
#%%
# Only compare less than equal for 1 hamming distant and add edge
idx = np.where(adj_mat)
adj_dist = (df.iloc[:,idx[0]].values <= df.iloc[:,idx[1]].values).all(axis=0)
adj_mat[idx[0],idx[1]] = adj_dist
#%%
G = nx.from_numpy_array(adj_mat, create_using=nx.DiGraph,nodelist=df.columns)
# %%
nx.draw(G,with_labels=True)
# %%
intervals = pd.DataFrame(0, index=G.nodes, columns=G.nodes, dtype=int)
# Fill the matrix with the unique node counts, excluding source and target
for source, target_paths in nx.all_pairs_all_shortest_paths(G):
    for target, paths in target_paths.items():
        all_nodes = set()
        for path in paths:
            all_nodes.update(path)
        # all_nodes -= {source,target}
        intervals.at[source, target] = len(all_nodes)
# %%
def interval_hmap(intervals, pfx):
    unique_vals = np.unique(intervals.values)
    print(unique_vals)
    fig, ax = plt.subplots()
    sns.heatmap(intervals, cbar_kws={'ticks': unique_vals}, ax=ax,square=True)
    ax.set_ylabel('Source (U)')
    ax.set_xlabel('Target (L)')
    fig.tight_layout()
    plt.savefig(f'./figures/Intervals/{pfx}-intervals.svg')
#%%
interval_hmap(intervals, pfx=f'B{n}-fn')
# %%
LUinter = intervals.iloc[U,L]
LUinter.columns = df.index
LUinter.index = df.index
# %%
interval_hmap(LUinter,pfx=f'B{n}-input')
# %%

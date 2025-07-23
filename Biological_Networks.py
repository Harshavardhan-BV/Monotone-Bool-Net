#%%
import os
import numpy as np
import pandas as pd
import networkx as nx
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, fcluster
plt.rcParams['svg.hashsalt'] = ''
os.makedirs('figures/Bionet', exist_ok=True)
os.makedirs('Output/Bionet', exist_ok=True)
#%%
# topo = 'EMT22N'
# topo = 'SCLC'
topo = 'Pluripotency'
#%%
df = pd.read_csv(f'./Inputs/Topo_bionet/{topo}.topo', sep=r'\s+')
df.rename(columns={df.columns[2]: 'weight'}, inplace=True)
df[df.columns[2]] = df[df.columns[2]].replace(2,-1)
# %%
G = nx.from_pandas_edgelist(df, source=df.columns[0], target=df.columns[1], edge_attr=df.columns[2], create_using=nx.DiGraph)
# %%
indeg = pd.Series(dict(G.in_degree))
print("Max indegree:", indeg.max())
print("Node(s) with max indegree:", indeg[indeg == indeg.max()].index.tolist())
indeg
#%%
adjmat = nx.to_pandas_adjacency(G)
# %%
all_sol = []
for node in G.nodes:
    if indeg[node] == 0:
        continue
    if adjmat.loc[node,node] == -1:
        print('NOOOOOOOOOOOOOOOOOO',node)
    inpt = adjmat.loc[:,node]
    inpt.at[node] = 1
    all_sol.append(inpt)
    all_sol.append(-inpt)
# %%
all_sol = pd.DataFrame(all_sol)
all_sol.replace(0, np.nan, inplace=True)
all_sol.replace(-1, 0, inplace=True)
# %%
sns.clustermap(all_sol, cmap='coolwarm', metric='hamming', yticklabels=False)
plt.savefig(f'figures/Bionet/IdealInput_clust_{topo}.svg')
# %%
Z = linkage(all_sol, metric='hamming', method='average')
labels = fcluster(Z, 2, criterion='maxclust')
# %%
grouped_df = all_sol.groupby(labels).agg(lambda x: x.value_counts().index[0]).astype(int)
grouped_df.to_csv(f'./Output/Bionet/{topo}-max-ss.csv')
# %%

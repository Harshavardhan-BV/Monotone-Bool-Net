#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import itertools as it
plt.rcParams['svg.hashsalt']=''
#%%
n = 2
stab = 2
topo = (1,1)
#%%
max = len(pd.read_csv(f'../Output/IO/MBF_B{n-1}.csv', header=None))
names = pd.read_csv(f'../Output/IO/MBF_B{n-1}_names.csv', header=None).iloc[:,0]
#%%
df = pd.read_csv(f'../Output/Multi/{n}-node_{stab}-stable_topo-{topo}_params.csv')
# %%
def pairgrid_heatmap(x, y, **kwargs):
    # Compute normalized 2D histogram (joint frequency table)
    density = pd.crosstab(x, y, normalize=True).T
    density = density.reindex(index=np.arange(max-1, -1, -1), columns=np.arange(0, max), fill_value=0)
    density.index = pd.Index(names[::-1], name=density.index.name)
    density.columns = pd.Index(names, name=density.columns.name)
    sns.heatmap(density, vmin=0, vmax=1, cmap='Spectral_r', cbar=False, **kwargs)

def pairgrid_barplot(x, **kwargs):
    # Compute normalized value counts
    counts = pd.Series(x).value_counts(normalize=True).reindex(np.arange(0, max), fill_value=0)
    counts.index = names
    ax = sns.barplot(x=counts.index, y=counts.values, **kwargs)
    ax.set_ylim(0,1)
#%%
g = sns.PairGrid(df, diag_sharey=False, corner=True)
g.map_diag(pairgrid_barplot)
g.map_lower(pairgrid_heatmap)
g.tight_layout()
plt.savefig(f'../figures/Multi/{n}-node-{stab}-stable-topo={topo}_params.svg')
# %%

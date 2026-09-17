# %%
import os
import mbnet as mn
import matplotlib.pyplot as plt
plt.rcParams['svg.hashsalt'] = ''
# %%
topofol = 'SinglePositive/Input/topofiles_3/'
topos = os.listdir(path=topofol)
# %%
ordc = mn.utils._readfiles(f'MBF_B2_names.csv')[0].values
# %%
def topo_PG(topo):
    adjmat = mn.utils.topo_to_adj(topofol+topo)
    ps = mn.tl.param_set(adjmat)
    fig,ax = plt.subplots(len(ordc), figsize=(4,4*len(ordc)))
    for i, funC in enumerate(ordc):
        pssub = ps[ps.loc[:,'C'] == funC]
        mn.pl.PG(pssub, 'A', 'B', (2, 2), ax=ax[i], vmin=0, vmax=3, cbar=False)
        ax[i].set_title(funC)
    fig.supylabel('C')
    fig.tight_layout()
    fig.savefig(f'figures/PG/PG_{topo.replace('.topo','')}.svg')
# %%
for topo in topos:
    topo_PG(topo)
# %%


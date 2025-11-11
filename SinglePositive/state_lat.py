#%%
import os
import glob
import numpy as np
import pandas as pd
import mbfnet as mn
import argparse
from multiprocessing import Pool
#%%
n = 6
#%%
topodir = f'Input/topofiles_{n}'
#%%
eqpot = pd.read_csv(f'Output/Equipotent/Equipotent_topofiles_{n}.txt',sep='\t', header=None).iloc[:,0]
#%%
# Single high states 10..0, 01..0, ...,00..1
sstate = np.eye(n, dtype=int).astype(str)
sstate = np.apply_along_axis(''.join, 0, sstate).tolist()
#%%
print(f"Number of topology files: {len(eqpot)}")
#%%
lul = []
for topo in eqpot:
    df = mn.tl.lat_mbm_topo(topodir+'/'+topo).loc[sstate]
    lul.append(df)
#%%
lul = pd.concat(lul, keys=eqpot)
#%%
lul.to_csv(f'./Output/Equipotent/Equipotent_lattice_{n}.csv')
# %%

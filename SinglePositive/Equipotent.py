#%%
import os
import numpy as np
import pandas as pd
#%%
n = 5
#%%
df = pd.read_csv(f'Output/Counts/Counts_topofiles_{n}.csv', index_col=0)
#%%
# Read the counts
n = 6
df = pd.read_csv(f'Output/Counts/Counts_topofiles_{n}.csv.gz', index_col=0)
df = df.astype(np.float64)
# %%
# Single high states 10..0, 01..0, ...,00..1
sstate = np.eye(n, dtype=int).astype(str)
sstate = np.apply_along_axis(''.join, 0, sstate).tolist()
# %%
# Select only the single high states and check if all of them are equal(implemented as all equal to 10..0)
scount = df.loc[:,sstate]
equipotent = scount.eq(scount.iloc[:,0],axis=0).all(axis=1)
# %%
equipotent = scount.loc[equipotent,:].iloc[:,0].to_frame(name='nMBM')
equipotent['LargestRelative'] = ~df.loc[equipotent.index].gt(equipotent.iloc[:,0],axis=0).any(axis=1)
#%%
# Save the list of topos
os.makedirs('Output/Equipotent',exist_ok=True)
equipotent.to_csv(f'Output/Equipotent/Equipotent_topofiles_{n}.txt', header=False, sep='\t')
# %%

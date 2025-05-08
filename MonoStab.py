#%%
import numpy as np
import pandas as pd
from common_func import gen_inps, multi_satish
#%%
n = 4
inp_class = pd.read_csv(f'./Output/Multi/{n}-node_{n}-stable_classes.csv').values[0,:-1]
monostab = pd.read_csv(f'Output/Multi/{n}-node_{n}-stable_states.csv', header=None).values[0,:]
#%%
inps = gen_inps(n)
# %%
inpfunc = multi_satish(inps, inp_class)
#%%
# Choose all functions which has atleast one 10* as stable
stable = inpfunc.loc[pd.MultiIndex.from_tuples([monostab])]
#%%
# Choose outputs of the functions that give 10* stable
mask = inpfunc.apply(lambda row: any((row.values == stable_row).all() for stable_row in stable.values), axis=1)
monostab_df = inpfunc.loc[mask]
#%%
# Count number of stable points
monostab_df = monostab_df.value_counts()
#%%
# Choose indices which 
monostab_df = monostab_df.index[monostab_df==1].to_frame(index=False)
#%%
monostab_df.to_csv(f'./Output/Monostab/{n}-node_topo-{inp_class}_monostab-{monostab}_params.csv', index=False)
# %%

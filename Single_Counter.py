#%%
import os
import numpy as np
import pandas as pd
from common_func import df_index, read_IO
os.makedirs('./Output/Count',exist_ok=True)
#%%
def freq_index(df, f):
    n = df.index.nlevels
    freqi = df_index(df,f[0]).loc[tuple(np.zeros(n))].sum()
    for j in range(0, n):
        mask = np.zeros(n)
        mask[j] = 1
        freqi *= (Dk - df_index(df,f[j+1]).loc[tuple(mask[::-1])].sum())
    return freqi
#%%
for n in range(2,5):
    df = read_IO(n)
    #%%
    ninputs = df.shape[0]
    Dk = df.shape[1]
    Tot_freq = Dk ** n
    #%%
    findex = pd.MultiIndex.from_product([range(ninputs)]*n, names=[f'f{i}' for i in range(n)])
    #%%
    df_count = pd.DataFrame(index=findex, columns=['Freq'])
    #%%
    for i in range(len(df_count)):
        f = df_count.index[i]
        df_count.iloc[i] = freq_index(df, f)
    #%%
    for i in range(df_count.index.nlevels):
        # Reorder by shifting the order right
        new_index = df_count.index.to_frame(index=False)
        new_index = np.roll(new_index, i, axis=1)
        new_index = pd.MultiIndex.from_arrays(new_index.T, names=df_count.index.names)
        # Add a new columns where the orders are shifted
        new_values = df_count['Freq'].reindex(new_index)
        new_values.index = df_count.index
        df_count[f'X{i}'] = new_values
    #%%
    # Drop the Freq column
    df_count.drop(columns='Freq', inplace=True)
    #%%
    # Sort by which has the highest sum
    df_count['Sum'] = df_count.sum(axis=1)
    df_count.sort_values(by='Sum', ascending=False, inplace=True)
    # %%
    df_count.to_csv(f'Output/Count/{n}-node_count.csv')
# %%

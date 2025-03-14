#%%
import numpy as np
import pandas as pd
#%%
n = 4 # Number of nodes
#%%
def df_index(df, j):
    # Convert j to a binary representation and make it an array
    index = df.index.to_frame(index=False)
    j = np.fromiter(np.binary_repr(j, width=index.shape[1]), dtype=int)
    new_index = (index  + j) % 2
    new_index = pd.MultiIndex.from_frame(new_index, names=[f'X{i}' for i in range(index.shape[1])])
    df1 = df.loc[new_index]
    df1.index = df.index
    return df1

def freq_index(df, f):
    n = df.index.nlevels
    freqi = df_index(df,f[0]).loc[tuple(np.zeros(n))].sum()
    for j in range(0, n):
        mask = np.zeros(n)
        mask[j] = 1
        freqi *= (Dk - df_index(df,f[j+1]).loc[tuple(mask[::-1])].sum())
    return freqi
#%%
inputs = pd.read_csv(f'Output/Inputs_B{n-1}.csv', header=None)
indx = pd.MultiIndex.from_frame(inputs)
df = pd.read_csv(f'Output/MBF_B{n-1}.csv', header=None, names=indx).T
df.sort_index(inplace=True)
#%%
ninputs = df.shape[0]
Dk = df.shape[1]
Tot_freq = n ** Dk
#%%
findex = pd.MultiIndex.from_product([range(ninputs)]*n, names=[f'f{i}' for i in range(n)])
#%%
df_count = pd.DataFrame(index=findex, columns=['Freq'])
#%%
for i in range(len(df_count)):
    f = df_count.index[i]
    df_count.iloc[i] = freq_index(df, f)
# %%
df_count.sort_values(by='Freq', ascending=False, inplace=True)
df_count.to_csv(f'Output/{n}-node_count.csv')
# %%

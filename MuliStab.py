#%%
import numpy as np
import pandas as pd
#%%
n = 2 # Number of nodes
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

def inpclass_multi_satisfy(multi, df):
    # Provide the steady states we want to have as multi-stable as rows
    inpclass_all = {}
    for i in range(n):
        # Map the input and output to satisfy the multi-stability
        multi_out = multi[:,0]
        multi_idx = np.delete(multi,0, axis=1)
        multi_df = pd.Series(multi_out, index=pd.MultiIndex.from_arrays(multi_idx.T))
        multi_df.sort_index(inplace=True)
        inpclass = []
        # Iterate over all input classes
        for j in range(2**(n-1)):
            df_j = df_index(df, j)
            bleh = df_j.loc[multi_df.index].eq(multi_df, axis=0).all(axis=0).any()
            if bleh:
                inpclass.append(j)
        inpclass_all[i] = inpclass
    return pd.DataFrame(inpclass_all)
#%%
inputs = pd.read_csv(f'Output/Inputs_B{n-1}.csv', header=None)
indx = pd.MultiIndex.from_frame(inputs)
df = pd.read_csv(f'Output/MBF_B{n-1}.csv', header=None, names=indx).T
df.sort_index(inplace=True)
#%%
multi = np.empty((0,n), dtype=int)
for j in range(0, n):
    mask = np.zeros(n, dtype=int)
    mask[j] = 1
    multi = np.vstack((multi, mask))
np.savetxt(f'Output/{n}-node_multistable-states.csv', multi, fmt='%d', delimiter=',')
# %%
multi_class = inpclass_multi_satisfy(multi, df)
# %%
multi_class.to_csv(f'Output/{n}-node_multistable-classes.csv', index=False)
# %%

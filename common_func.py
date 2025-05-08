import numpy as np
import pandas as pd
from itertools import product

def gen_inps(n):
    # Generate all possible inputs
    inputs = np.array(np.meshgrid(*[[0, 1]]*n)).T.reshape(-1, n)
    return inputs

def read_IO(n):
    inputs = pd.read_csv(f'Output/IO/Inputs_B{n-1}.csv', header=None)
    indx = pd.MultiIndex.from_frame(inputs)
    df = pd.read_csv(f'Output/IO/MBF_B{n-1}.csv', header=None, names=indx).T
    df.sort_index(inplace=True)
    return df

def df_index(df, j):
    # Convert j to a binary representation and make it an array
    index = df.index.to_frame(index=False)
    j = np.fromiter(np.binary_repr(j, width=index.shape[1]), dtype=int)
    new_index = (index  + j) % 2
    new_index = pd.MultiIndex.from_frame(new_index, names=[f'X{i}' for i in range(index.shape[1])])
    df1 = df.loc[new_index]
    df1.index = df.index
    return df1

def df_sub(df_j,i, func_i, func_u):
    if func_u[i]:
        df_j = df_j.loc[:,df_j.columns>=func_i[i]]
    else:
        df_j = df_j.loc[:,df_j.columns<=func_i[i]]
    return df_j

def df_multio(multi,i, sort=True):
    multii = np.roll(multi, -i, axis=1)
    multi_out = multii[:,0]
    multi_idx = np.delete(multii,0, axis=1)
    multi_df = pd.Series(multi_out, index=pd.MultiIndex.from_arrays(multi_idx.T))
    if sort:
        multi_df.sort_index(inplace=True)
    return multi_df

def multi_satish(inps, inp_class):
    if inps.shape[1] != len(inp_class):
        raise ValueError('Input size has to match the number of Input class')
    inpfunc = {}
    n = inps.shape[1]
    df = read_IO(n)
    for i in range(n):
        multi_df = df_multio(inps, i, sort=False)
        df_j = df_index(df, inp_class[i])
        # Find columns where the state is stable
        mask = df_j.loc[multi_df.index].eq(multi_df, axis=0)
        # For each row, get the column names where the value is True
        bleh = mask.apply(lambda row: list(row.index[row]), axis=1)
        inpfunc[f'p{i}'] = bleh.values
    outdf = pd.DataFrame()
    for j in range(inps.shape[0]):
        # Make combinations
        class_comb = list(product(*(inpfunc[idx][j] for idx in inpfunc.keys())))
        if not class_comb:
            continue #if empty
        # class_comb = pd.DataFrame([inps[j,:]]*len(class_comb), index=pd.MultiIndex.from_tuples(class_comb, names=list(inpfunc.keys())))
        class_comb = pd.DataFrame(class_comb, index=pd.MultiIndex.from_tuples([inps[j,:]]*len(class_comb)),columns=list(inpfunc.keys()))
        outdf = pd.concat([outdf,class_comb])
    return outdf
import os
import glob
import numpy as np
import pandas as pd
import itertools as it

def df_index(df, j):
    # Convert j to a binary representation and make it an array
    index = df.index.to_frame(index=False)
    j = np.fromiter(np.binary_repr(j, width=index.shape[1]), dtype=int)
    new_index = (index  + j) % 2
    new_index = pd.MultiIndex.from_frame(new_index, names=[f'X{i}' for i in range(index.shape[1])])
    df1 = df.loc[new_index]
    df1.index = df.index
    return df1

def inpclass_multi_satisfy(multi, df, n):
    # Provide the steady states we want to have as multi-stable as rows
    inpclass_all = {}
    for i in range(n):
        # Map the input and output to satisfy the multi-stability
        multii = np.roll(multi, -i, axis=1)
        multi_out = multii[:,0]
        multi_idx = np.delete(multii,0, axis=1)
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
    return inpclass_all

def multi_class(fname):
    multi = pd.read_csv(f'Output/Multi/{fname}', header=None)
    n = multi.shape[1]
    inputs = pd.read_csv(f'Output/IO/Inputs_B{n-1}.csv', header=None)
    indx = pd.MultiIndex.from_frame(inputs)
    df = pd.read_csv(f'Output/IO/MBF_B{n-1}.csv', header=None, names=indx).T
    df.sort_index(inplace=True)
    mc = inpclass_multi_satisfy(multi, df, n)
    outname = fname.replace('_states','_classes')
    class_comb = list(it.product(*(mc[idx] for idx in mc.keys())))
    class_comb = pd.DataFrame(class_comb, columns=[f'f{i}' for i in range(n)])
    class_comb.to_csv(f'Output/Multi/{outname}', index=False)

fnames = glob.glob('*_states.csv', root_dir='Output/Multi/')
for fname in fnames:
    multi_class(fname)


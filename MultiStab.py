import os
import glob
import numpy as np
import pandas as pd
import itertools as it
from common_func import multi_satish

def inpclass_multi_satisfy(multi, topo, fname):
    inpclass = multi_satish(multi,topo)
    class_comb = (inpclass.value_counts() == multi.shape[0])
    class_comb = class_comb.index[class_comb].to_frame(index=False)
    if len(class_comb)>0:
        class_comb.to_csv(f'Output/Multi/{fname}_topo-{topo}_params.csv', index=False)
    return len(class_comb)

def multi_class(fname):
    # Read the multistable array where each row represents a state
    multi = pd.read_csv(f'Output/Multi/{fname}', header=None).values
    n = multi.shape[1]
    # Iterate over all the topology classes 
    topo_class = list(it.product(range(2**(n-1)), repeat=n))
    fname = fname.replace('_states.csv','')
    counts = []
    for topo in topo_class:
        # Find parameters that satisfy stability of multi for a given topology
        counts.append(inpclass_multi_satisfy(multi, topo, fname))
    class_comb = pd.DataFrame(topo_class, columns=[f'f{i}' for i in range(n)])
    class_comb['n_params'] = counts
    class_comb = class_comb[class_comb['n_params']>0]
    class_comb.to_csv(f'Output/Multi/{fname}_classes.csv', index=False)

fnames = glob.glob('*_states.csv', root_dir='Output/Multi/')
for fname in fnames:
    print(fname)
    multi_class(fname)


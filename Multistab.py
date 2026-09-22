#%%
import os
import mbnet as mn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from multiprocessing import Pool
plt.rcParams['svg.hashsalt'] = ''
# %%
n = 3
topofol = f'Inputs/Topo/topofiles_{n}/'
topos = os.listdir(path=topofol)
#%%
states = mn.utils.B(n)
# %%
def ms_count(topo):
    adjmat = mn.utils.topo_to_adj(topofol + topo)
    mscount = []
    
    for nstable in range(2, len(states) + 1):
        if nstable == 2:
            # Brute force for nstable=2
            valid_combinations =  list(combinations(states, nstable))
        else:
            # For nstable >= 3, generate combinations only from valid (n-1)-stable cases
            valid_pairs = np.array(valid_pairs)
            valid_combinations = []

            # Generate all possible combinations of size nstable from the valid pairs
            for combo in combinations(valid_pairs, nstable):
                # Flatten the combination and remove duplicates
                flattened = np.vstack(combo)
                unique_states, indices = np.unique(flattened, axis=0, return_index=True)
                unique_indices = sorted(indices)

                # Only keep combinations that have exactly nstable unique states
                if len(unique_indices) == nstable:
                    valid_combinations.append(unique_states)
        valid_pairs = []
        # Check each valid combination
        for msstates in valid_combinations:
            msstates = pd.DataFrame(msstates, columns=adjmat.columns)
            nmbm = len(mn.tl.multistable(adjmat, msstates))
            if nmbm > 0:
                mscount.append([topo, nstable, '-'.join(msstates.astype(str).agg(''.join, axis=1)), nmbm])
                valid_pairs.append(msstates.values)
    return pd.DataFrame(mscount, columns=['topo','nstable','states','nMBM'])
#%%
if __name__ == "__main__":
    with Pool(os.cpu_count()-2) as pool:
        mscount = pool.map(ms_count, topos)
    mscount = pd.concat(mscount)
    mscount = mscount.pivot(columns=['topo'], index=['nstable','states'], values='nMBM').T
    mscount = mscount.fillna(0).astype(int)
    mscount.to_csv(f'Output/Counts/MSCounts_topofiles_{n}.csv')
# %%

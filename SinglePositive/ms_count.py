#%%
import os
import numpy as np
import pandas as pd
import mbnet as mn
from multiprocessing import Pool

n = 6
save = True

def adj_full(n,m):
    """
    Gives adjacency matrix of a fully connected network with self activations and inhibitions to node 0 from the first m.
    """
    adjmat = pd.DataFrame(np.ones((n,n),dtype=int))
    adjmat.loc[1:m,0] = -1
    return adjmat


def count_one(m):
    BLi = mn.tl.lattice_B(n)
    sstate = pd.DataFrame(np.eye(n, dtype=int))
    A = adj_full(n, m)
    inp, oup = mn.utils.T(A, sstate, 0)
    inp = pd.DataFrame(inp).astype(str).sum(axis=1)
    mn.tl.constraint_IO(BLi, inp, oup)
    if save:
        mn.pl.lattice(BLi, f'figures/Lattice/B{n}-{m}.svg')
    return [n, m, mn.tl.unconstrained_count(BLi)]


if __name__ == "__main__":
    with Pool(os.cpu_count()-2) as pool:
        Wi = pool.map(count_one, range(n))
    Wi = pd.DataFrame(Wi, columns=['n','m','|Wi|'])
    Wi.to_csv(f'./Output/Multistable/Count-{n}.csv')
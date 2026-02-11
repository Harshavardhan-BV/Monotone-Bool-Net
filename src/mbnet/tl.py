import numpy as np
import pandas as pd
import mbnet as mn
import networkx as nx
from scipy.spatial.distance import pdist, squareform

def n_mbm(adjmat):
    """
    Computes the number of monotone Boolean functions (MBFs) for each Boolean state for a given network topology.

    Parameters
    ----------
    adjmat: pd.DataFrame
        Adjacency matrix of the network topology.
    
    Returns
    -------
    pd.DataFrame
        DataFrame containing the number of MBF for each target node and the total product across all nodes. The index gives the Boolean state in same order as the columns.
    """
    n = adjmat.shape[1]
    bBn = mn.utils.B(n)
    bBn = pd.DataFrame(bBn,columns=adjmat.columns)
    nMBF = pd.DataFrame(columns=bBn.columns, index=bBn.index)
    for tgt in adjmat.columns:
        inps = adjmat.loc[:,tgt]
        inpt = ((1 - inps) // 2) + inps * bBn
        inpt = inpt.loc[:,inps!=0].sum(axis=1)
        oupt = bBn.loc[:,tgt]
        k = inps.abs().sum()
        nMBF.loc[:,tgt] = inpt.apply(lambda i: mn.utils.U(k, i))
        nMBF.loc[oupt==0,tgt] = mn.utils.D(k) - nMBF.loc[oupt==0,tgt]
    nMBF.index = bBn.astype(str).sum(axis=1)
    nMBF['Total'] = nMBF.product(axis=1)
    return nMBF

def UL_mbm(adjmat):
    """
    Lattice representation of monotone Boolean functions (MBFs) for each Boolean state for a given network topology.

    Parameters
    ----------
    adjmat: pd.DataFrame
        Adjacency matrix of the network topology.
    
    Returns
    -------
    pd.DataFrame
        DataFrame containing the lattice representation of MBF for each target node. The index gives the Boolean state in same order as the columns.
    """
    n = adjmat.shape[1]
    bBn = mn.utils.B(n)
    bBn = pd.DataFrame(bBn,columns=adjmat.columns)
    nMBF = pd.DataFrame(columns=bBn.columns, index=bBn.index)
    for tgt in adjmat.columns:
        inps = adjmat.loc[:,tgt]
        inpt = ((1 - inps) // 2) + inps * bBn
        inpt = inpt.loc[:,inps!=0]
        oupt = bBn.loc[:,tgt]
        nMBF.loc[:,tgt] = oupt.replace({1:'U(',0:'L('}) + inpt.astype(str).sum(axis=1) + ')'
    nMBF.index = bBn.astype(str).sum(axis=1)
    return nMBF

def lattice_B(n:int):
    """
    Construct the Boolean lattice as a directed graph.

    Parameters
    ----------
    n : int
        Dimension of the Boolean vector. Must be a non-negative integer.

    Returns
    -------
    networkx.DiGraph
        A directed graph representing the n-dimensional Boolean lattice.
        - Nodes: Boolean vectors as strings.
        - Node attribute "level": Number of 1s of the node.
        - Directed edges: (u -> v) whenever v is obtained from u by flipping exactly one 0 to 1 (Partially ordered).

    Notes
    -----
    - The graph contains 2**n nodes. Time and memory costs grow exponentially with n.
    - The function uses pairwise Hamming distances to identify candidate edges and then orients them from lower to higher bitwise vectors.
    """
    df = pd.DataFrame(mn.utils.B(n))
    df.index = df.astype(str).sum(axis=1)
    lvl = df.sum(axis=1)
    # Calculate Hamming distances between all pairs of columns and choose only those 1 away
    adj_mat = squareform(pdist(df, metric='hamming'))
    adj_mat = (adj_mat == 1/n)
    # Only compare less than equal for 1 hamming distant and add edge
    idx = np.where(adj_mat)
    adj_dist = (df.T.iloc[:,idx[0]].values <= df.T.iloc[:,idx[1]].values).all(axis=0)
    adj_mat[idx[0],idx[1]] = adj_dist
    G = nx.from_numpy_array(adj_mat, create_using=nx.DiGraph,nodelist=df.index)
    nx.set_node_attributes(G, lvl, "level")
    return G
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

def lattice(df):
    """
    Constructs a directed lattice graph from a DataFrame of binary vectors.

    Parameters
    ----------
    df : pd.DataFrame
        A DataFrame where each row represents a binary vector and each column represents a dimension.
        The index of the DataFrame will be used as node names in the resulting graph.

    Returns
    -------
    networkx.DiGraph
        A directed graph representing the lattice structure of the input vectors.
        - Nodes: Named according to the DataFrame index.
        - Node attribute "level": Sum of 1s in each binary vector.
        - Directed edges: (u -> v) whenever v is obtained from u by flipping exactly one 0 to 1 (Partially ordered).

    Notes
    -----
    - Edges are directed from lower to higher vectors in the partial order.
    - The function identifies candidate edges by computing pairwise Hamming distances and keeps only those exactly 1 unit apart.
    - Edge orientation is determined by element-wise comparison of the binary vectors.
    """
    lvl = df.sum(axis=1)
    # Calculate Hamming distances between all pairs of columns and choose only those 1 away
    adj_mat = squareform(pdist(df, metric='hamming'))
    adj_mat = (adj_mat == 1/df.shape[1])
    # Only compare less than equal for 1 hamming distant and add edge
    idx = np.where(adj_mat)
    adj_dist = (df.T.iloc[:,idx[0]].values <= df.T.iloc[:,idx[1]].values).all(axis=0)
    adj_mat[idx[0],idx[1]] = adj_dist
    G = nx.from_numpy_array(adj_mat, create_using=nx.DiGraph,nodelist=df.index)
    nx.set_node_attributes(G, lvl, "level")
    return G

def lattice_B(n:int):
    """
    Constructs the lattice as a directed graph for n-dimensional Boolean vectors.

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
    return lattice(df)

def lattice_MBF(n:int):
    """
    Constructs the lattice as a directed graph for monotone Boolean functions with n inputs.

    Parameters
    ----------
    n : int
        The number of inputs for the monotone Boolean functions (MBF). Must be a non-negative integer.
    
    Returns
    -------
    networkx.DiGraph
        A directed graph representing the n-input MBF lattice.
        - Nodes: MBF names.
        - Node attribute "level": Number of 1 outputs of the function.
        - Directed edges: (u -> v) if the truth set of u is a subset of the truth set of v.
    """
    df = mn.utils.MBF(n).T
    return lattice(df)

def param_set(adjmat, explode=True):
    """
    Gives the set of parameter sets (MBF combinations) for each Boolean state for a given network topology.

    Parameters
    ----------
    adjmat: pd.DataFrame
        Adjacency matrix of the network topology.
    explode: Bool, default=True
        If True, explodes the resulting DataFrame to individual rows for each MBF combination.
        If False, each cell contains a set of valid MBF combinations.

    Returns
    -------
    pd.DataFrame
        A DataFrame with columns corresponding to target nodes.
        Each row contains either a set of valid MBF combinations (when explode=False) or individual MBF combinations (when explode=True).
        The Boolean state is given in a 'state' column (when explode=True), otherwise as the index.

    Notes
    -----
    - Uses mn.utils.L_set() for targets with output value 0
    - Uses mn.utils.U_set() for targets with output value 1
    """
    n = adjmat.shape[1]
    bBn = mn.utils.B(n)
    bBn = pd.DataFrame(bBn,columns=adjmat.columns)
    MBF_set = pd.DataFrame(columns=bBn.columns, index=bBn.index)
    for tgt in adjmat.columns:
        inpt, oupt = mn.utils.T(adjmat,bBn,tgt)
        MBF_set.loc[:, tgt] = inpt.apply(
            lambda row: mn.utils.L_set(row) if oupt.loc[row.name] == 0 else mn.utils.U_set(row),
            axis=1
        )
    MBF_set.index = bBn.astype(str).sum(axis=1)
    if explode:
        for tgt in MBF_set.columns:
            MBF_set = MBF_set.explode(tgt)
        MBF_set.reset_index(inplace=True, names='state')
    return MBF_set

def multistable(adjmat, states, explode=True):
    """
    Gives parameter combinations that support multistability between the given states for a given topology.
    
    Parameters
    ----------
    adjmat: pd.DataFrame
        Adjacency matrix of the network topology.
    states: pd.DataFrame
        DataFrame containing the states to consider for multistability.
    explode: bool, default=True
        If True, explodes the parameter sets into separate rows for each parameter combination.
    Returns
    -------
    pd.DataFrame
        A DataFrame where each column corresponds to a target node and each cell contains a set of MBF combinations that support multistability between the given states.
        If explode is True, the sets are expanded into MBF combinations.
    Notes
    -----
    This function identifies multistable functions by taking the intersection of corresponding L_set and U_set's.
    """
    MBF_set = pd.DataFrame(columns=states.columns, index=[0])
    for tgt in adjmat.columns:
        inpt, oupt = mn.utils.T(adjmat,states,tgt)
        temp = inpt.apply(
            lambda row: mn.utils.L_set(row) if oupt.loc[row.name] == 0 else mn.utils.U_set(row),
            axis=1
        )
        MBF_set.loc[:, tgt] = set.intersection(*temp)
    if explode:
        for tgt in MBF_set.columns:
            MBF_set = MBF_set.explode(tgt)
            MBF_set.reset_index(inplace=True, drop=True)
    return MBF_set

    

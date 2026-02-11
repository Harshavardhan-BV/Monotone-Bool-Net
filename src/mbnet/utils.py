import mbnet.const
import numpy as np
import pandas as pd
import networkx as nx
from importlib import resources

def B(k:int):
    """
    Return all Boolean vectors of length k.

    Parameters
    ----------
    k : int
        Lenght of Boolean vector. Must be a positive integer.
    
    Returns
    -------
    np.ndarray
        A 2**k by k array of integers (0 or 1) containing every binary combination of length k. 
    """
    if k <= 0:
        raise ValueError("k must be a positive integer.")
    return np.array(np.meshgrid(*[[0, 1]]*k)).T.reshape(-1, k)


def D(k:int):
    """
    Return the number of monotone Boolean functions (MBFs) on k input variables. This value is equivalent to the Dedekind numbers.

    Parameters
    ----------
    k : int
        Number of input variables. Must be a positive integer.
    
    Returns
    -------
    int
        Number of MBFs with k inputs.
    """
    if k <= 0:
        raise ValueError("k must be a positive integer.")
    try:
        return mbnet.const.Dk[k]
    except KeyError:
        raise NotImplementedError("Dedekind number not computed for k>9")

def U(k:int,i:int):
    """
    Return the number of monotone Boolean functions (MBFs) on k input variables that evaluate to 1 on inputs with exactly i ones (Hamming weight i). This value is equivalent to the size of the corresponding up-sets in the lattice of MBFs.

    Parameters
    ----------
    k : int
        Number of input variables. Must be a positive integer.
    
    i : int
        Number of 1s of input vectors. Must satisfy 0 <= i <= k.
    
    Returns
    -------
    int
        Number of MBFs that evaluate to 1 for inputs with i 1s
    """
    if k <= 0:
        raise ValueError("k must be a positive integer.")
    if k < i < 0:
        raise ValueError("i should be between 0 and k")
    try:
        return mbnet.const.phi[k][i]
    except KeyError:
        raise NotImplementedError("Not computed for MBFs with k>5")

def L(k:int,i:int):
    """
    Return the number of monotone Boolean functions (MBFs) on k input variables that evaluate to 0 on inputs with exactly i ones (Hamming weight i). This value is equivalent to the size of the corresponding up-sets in the lattice of MBFs.

    Parameters
    ----------
    k : int
        Number of input variables. Must be a positive integer.
    
    i : int
        Number of 1s of input vectors. Must satisfy 0 <= i <= k.
    
    Returns
    -------
    int
        Number of MBFs that evaluate to 0 for inputs with i 1s
    """
    return D(k) - U(k,i)
    

def topo_to_adj(topo:str):
    """
    Convert a topology (.topo) file to an adjacency matrix. The topo file should be tab-seperated with source target type. Type: 1 -> Activation, 2 -> Inhibition.

    Parameters
    ----------
    topo : str
        The path to the topofile.
    
    Returns
    -------
    pd.DataFrame 
        The adjacency matrix. Rows: Source, Columns: Target
    """
    df = pd.read_csv(topo,sep=r'\s+')
    df[df.columns[2]] = df[df.columns[2]].replace(2,-1)
    G = nx.from_pandas_edgelist(df, source=df.columns[0], target=df.columns[1], edge_attr=df.columns[2], create_using=nx.DiGraph)
    adjMat = nx.to_pandas_adjacency(G, weight=df.columns[2], nonedge=0)
    adjMat.loc[pd.Series(dict(G.out_degree())) > 0,pd.Series(dict(G.in_degree())) > 0]
    return adjMat

def _readfiles(fname):
    # Read from package data
    inputs_data = resources.files('mbnet').joinpath('mbfs', fname).read_text()
    return pd.read_csv(__import__('io').StringIO(inputs_data), header=None)

def MBF(k):
    """
    Loads the precomputed Monotone Boolean Functions (MBFs) for k inputs.

    Parameters
    ----------
    k : int
        The number of inputs for which to load MBF data.

    Returns
    -------
    pd.DataFrame 
        DataFrame containing MBF values indexed by input combinations. Column names for the functions are included if available.

    Raises
    ------
    FileNotFoundError 
        If the required input files are not found.
    """
    inputs = _readfiles(f'Inputs_B{k}.csv')
    indx = pd.MultiIndex.from_frame(inputs)
    df = _readfiles(f'MBF_B{k}.csv').T
    df.index = indx
    try:
        column_names = _readfiles(f'MBF_B{k}_names.csv').iloc[:, 0]
        df.columns = column_names
    except FileNotFoundError:
        pass
    df.sort_index(inplace=True)
    return df
import pandas as pd
import mbfnet as mn

def n_mbm_topo(topo:str):
    """
    Computes the number of monotone Boolean functions (MBFs) for each Boolean state for a given network topology.

    Parameters
    ----------
        topo: str
            Path to the topology file. topo file should be compatible with `mn.utils.topo_to_adj`.
    
    Returns
    -------
        pd.DataFrame: DataFrame containing the number of MBF for each target node and the total product across all nodes. The index gives the Boolean state in same order as the columns.
    """
    adjmat = mn.utils.topo_to_adj(topo)
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

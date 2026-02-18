import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import mbnet as mn
plt.rcParams['svg.hashsalt'] = ''

def lattice(G, save=False):
    """
    Plots a Hasse Diagram of a given Lattice. 

    The node are arranged vertically based on their "level" attribute (partial order).

    The nodes are colored based on their "value" attribute (Red : 1; Blue : 0; None : o/w).

    Parameters
    ----------
    G : networkx.DiGraph
        The input lattice (as a graph) to be visualized.
    save : bool or str 
        If string is provide, saves the figure to the specified filename. If False, the figure is not saved. Default is False.
    """
    levels = nx.get_node_attributes(G, "level")
    vals = nx.get_node_attributes(G, "value")
    node_colors = ['tab:red' if vals.get(n) == 1 else 'tab:blue' if vals.get(n) == 0 else 'None' for n in G.nodes()]
    pos = {}
    for lvl_val in sorted(set(levels.values())):
        nodes = sorted([n for n, v in levels.items() if v == lvl_val])
        # xs = np.arange(0, len(nodes))
        for i, n in enumerate(nodes):
            pos[n] = (i, lvl_val)  # vertical arranged by level
    nx.draw(G, pos=pos, with_labels=True, node_color=node_colors, node_shape='s')
    if save:
        plt.savefig(f'{save}')
    plt.show()

def PG(MBFs, x ,y, k=None ,save=False):
    """
    Plots the parameter graph based on the provided parameter set. 

    Parameters
    ----------
    MBFs: networkx.DiGraph
        The input lattice (as a graph) to be visualized.
    x : str
        Column name in MBFs to use as the x-axis (columns) of the parameter graph.
    y : str
        Column name in MBFs to use as the y-axis (rows) of the parameter graph.
    k : tuple (Optional)
        Number of inputs for function of x and y. Used for arraging the axes.
    save : bool or str 
        If string is provide, saves the figure to the specified filename. If False, the figure is not saved. Default is False.
    """
    nstable = MBFs.groupby([y, x]).size().unstack(fill_value=0)
    nstates = MBFs.groupby([y, x])['state'].apply('\n'.join).unstack(fill_value='')
    if isinstance(k, tuple):
        ordx = mn.utils._readfiles(f'MBF_B{k[0]}_names.csv')[0].values
        ordy = mn.utils._readfiles(f'MBF_B{k[1]}_names.csv')[0].values
        nstable = nstable.reindex(index=ordy[::-1], columns=ordx)
        nstates = nstates.reindex(index=ordy[::-1], columns=ordx)
    sns.heatmap(nstable, cmap='magma_r', linewidth=4, annot=nstates, fmt='s')
    if save:
        plt.savefig(f'{save}')
    plt.show()
# %%
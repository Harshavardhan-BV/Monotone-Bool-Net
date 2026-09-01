import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
import mbnet as mn
from itertools import product
from matplotlib.patches import FancyArrowPatch
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

def network(A):
    """
    Visualizes a network as a directed graph with circular layout.

    Plots nodes in a circular arrangement with edges colored and styled based on their sign. Positive edges are shown in red, negative edges in blue.

    Parameters
    ----------
    A : pandas.DataFrame
        Adjacency matrix representation of the network. Index and columns should contain node names.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure object containing the plot.
    ax : matplotlib.axes.Axes
        The axes object containing the plot.

    Notes
    -----
    The circular layout may not be ideal for all network types. The plots can get crowded for large networks.
    """
    
    edegprop = {
        1: ('red','->', 15),
        -1: ('blue','-[', 2)
    }
    ang = 60
    connprop = {
        True: 'arc,angleA=15, armA=30,rad=10, angleB=90, armB=30,rad=-10',
        False: 'arc3,rad=0.1'
    }
    # Plot the graph
    G = nx.from_pandas_adjacency(A, create_using=nx.DiGraph)
    # Get the positions
    pos = nx.circular_layout(G)
    # print(pos)
    # Draw nodes
    fig, ax = plt.subplots(figsize=(5,5))
    nx.draw_networkx_nodes(G, pos, node_color='none', alpha=1, node_size=1500, edgecolors='black', linewidths=1, margins=0.1)
    # plt.scatter(0,0, color='black', s=10)
    nx.draw_networkx_labels(G, pos, font_size=12)
    wt = list(list(G.edges(data=True))[0][-1].keys())[0]
    # Draw edges
    for sign in [1,-1]:
        for sign, selfe in product([1,-1],[False, True]):
            edges = [e for e in G.edges if (G.edges[e][wt] == sign) & ((e[0] == e[1]) == selfe)]
            if not selfe:
                nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edegprop[sign][0], arrowstyle=edegprop[sign][1], node_size=1500, width=2, alpha=0.5, arrowsize=edegprop[sign][2], connectionstyle=connprop[False], arrows=True, min_target_margin=25)
            else:
                # Draw the loops using matplotlib
                for edge in edges:
                    # Get the position of the node
                    posn = pos[edge[0]]
                    # Get the angles of node pos to the origin
                    angle = np.array([-ang,ang]) + np.arctan2(posn[1],posn[0]) * 180/np.pi
                    # Offset posn from the original point by 1500
                    posn1 = posn + 0.20* np.array([np.cos(angle[0]*np.pi/180), np.sin(angle[0]*np.pi/180)])
                    posn2 = posn + 0.20* np.array([np.cos(angle[1]*np.pi/180), np.sin(angle[1]*np.pi/180)])
                    # Make the loop as arcs with arrows coming out at thetas
                    ax.add_patch(FancyArrowPatch(posn1, posn2, connectionstyle='arc3, rad=2', edgecolor=edegprop[sign][0], arrowstyle=edegprop[sign][1], linewidth=2, alpha=0.5, mutation_scale=edegprop[sign][2]))
    return fig, ax
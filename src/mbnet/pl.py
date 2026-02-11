import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
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
#%%
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyArrowPatch
import networkx.algorithms.isomorphism as iso
import itertools as it
#%%
n = 4
#%%
def plot_graphTopo(G, layout='circular', ang=60):
    # Some switch cases
    layouts = {
        'circular': nx.circular_layout,
        'kamada_kawai': nx.kamada_kawai_layout,
        'random': nx.random_layout,
        'shell': nx.shell_layout,
        'spring': nx.spring_layout,
        'spectral': nx.spectral_layout,
        'spiral': nx.spiral_layout
    }
    edegprop = {
        1: ('red','->', 15),
        -1: ('blue','-[', 2)
    }
    connprop = {
        True: 'arc,angleA=15, armA=30,rad=10, angleB=90, armB=30,rad=-10',
        False: 'arc3,rad=0.1'
    }
    # Plot the graph
    # Get the positions
    pos = layouts[layout](G)
    print(pos)
    # Draw nodes
    fig, ax = plt.subplots(figsize=(5,5))
    nx.draw_networkx_nodes(G, pos, node_color=sns.color_palette('muted',n_colors=len(pos)), node_size=1500, edgecolors='black', linewidths=1, margins=0.1, ax=ax)
    # plt.scatter(0,0, color='black', s=10)
    nx.draw_networkx_labels(G, pos, font_size=12, ax=ax)
    # Draw edges
    for sign, selfe in it.product([1,-1],[False, True]):
        edges = [e for e in G.edges if (G.edges[e]['weight'] == sign) & ((e[0] == e[1]) == selfe)]
        if not selfe:
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=edegprop[sign][0], arrowstyle=edegprop[sign][1], node_size=1500, width=2, connectionstyle=connprop[selfe], min_target_margin=25, alpha=0.5, arrowsize=edegprop[sign][2], ax=ax)
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
    plt.tight_layout()
    return fig, ax

def bin_to_G(row):
    # Convert to binary array
    row_topo = np.array([list(np.binary_repr(int(x), width=n-1)) for x in row], dtype=int)
    row_topo[row_topo == 1] = -1
    row_topo[row_topo == 0] = 1
    adjmat = np.zeros((n,n))
    # adjmat = np.arange(n*n).reshape((n,n))
    for j in range(n):
        rolled = np.roll(adjmat[j,:], -j)
        rolled[1:] = row_topo[j]
        adjmat[j,:] = np.roll(rolled, j)
    G = nx.from_numpy_array(adjmat, create_using=nx.DiGraph)
    # Relabel nodes to A, B, C, ...
    mapping = {i: chr(65 + i) for i in range(n)}
    G = nx.relabel_nodes(G, mapping)
    return G

def non_iso_G(df):
    pass
#%%
df = pd.read_csv(f'../Output/Count/{n}-node_count.csv')
#%%
df_count = df.filter(regex=r'^X\d+$')
n = df_count.shape[1]
idx = np.unique(np.sort(df_count, 1), axis=0, return_index=True)[1]
df_iso = df.iloc[sorted(idx)]
df_topo = df_iso.filter(regex=r'^f\d+$')
# %%
for i in range(len(df_topo)):
    G = bin_to_G(df_topo.iloc[i])
    fig, ax = plot_graphTopo(G)
    counts = df_iso.filter(regex=r'^X\d+$').iloc[i].astype(str)
    x_text = ', '.join([f"{col}:{val}" for col, val in zip(counts.index, counts.values)])
    fig.text(0.5, 0.05, x_text, ha='center', fontsize=12)
    plt.savefig(f'../figures/Count/{n}-node-top_{i}.svg')
# %%

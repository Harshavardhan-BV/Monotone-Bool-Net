#!/usr/bin/env python

import argparse
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import itertools as it
plt.rcParams['svg.hashsalt'] = ''

parser = argparse.ArgumentParser(
    prog="MaxNet",
    description="Find the signs for a given network topology to maximize the frequency of a particular steady state"
)
parser.add_argument(
    "--topo", 
    type=str, 
    required=True,
    help="Input topology file name - only source target required"
)
parser.add_argument(
    "--ss", 
    type=str, 
    required=True,
    help="Steady state file name"
)
parser.add_argument(
    "--outtopo", 
    type=str, 
    help="Output topo file name"
)
parser.add_argument(
    "--plot", 
    action=argparse.BooleanOptionalAction, 
    default=True,
    help="Plot the graph of network"
)
args = parser.parse_args()

def topo_to_adj(topo_name):
    topo = pd.read_csv(topo_name, sep=r'\s+')
    G = nx.from_pandas_edgelist(topo, source=topo.columns[0], target=topo.columns[1], create_using=nx.DiGraph)
    return nx.to_pandas_adjacency(G,dtype=int)

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
    nx.draw_networkx_nodes(G, pos, node_color='white', node_size=1500, edgecolors='black', linewidths=1, margins=0.1, ax=ax)
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
    plt.show()
    return fig, ax

ss = pd.read_csv(args.ss)
adj_mat = topo_to_adj(args.topo)
adj_mat_sign = adj_mat.copy()

for node in ss.columns:
    # Select the index for inputs to function of node
    func = adj_mat.loc[:,node]
    if not func.sum():
        continue
    input_idx = func[func == 1].index
    # Select the input and output values
    input_val = ss.loc[0, input_idx]
    output_val = ss.loc[0, node]
    if output_val:
        # Choose for U -> 11...1 maximum
        # Change to negative if input 0
        sign = 2 * input_val - 1
    else:
        # Choose from L -> 00...0 maximum
        # Change to negative if input 1
        sign = -2 * input_val + 1
    adj_mat_sign.loc[input_idx,node] = sign

G = nx.from_pandas_adjacency(adj_mat_sign,create_using=nx.DiGraph)
topo = nx.to_pandas_edgelist(G)
topo['weight'] = topo['weight'].replace(-1,2)
if args.outtopo:
    topo.to_csv(args.outtopo)
else:
    print(topo.to_string(index=False))

if args.plot:
    plot_graphTopo(G)
#%%
import numpy as np
import pandas as pd
import mbnet as mn
import networkx as nx
import matplotlib.pyplot as plt
#%%
# topo = 'Inputs/Topo/Repressilator.topo'
topo = 'Inputs/Topo/TS.topo'
# topo = 'Inputs/Topo/NFL.topo'
#%%
adjmat = mn.utils.topo_to_adj(topo)
# # %%
G = nx.from_pandas_adjacency(adjmat,create_using=nx.DiGraph)
mn.pl.network(adjmat)
# %%
def STGen(adjmat):
    states = pd.DataFrame(mn.utils.B(len(adjmat)),columns=adjmat.columns)

    STG = pd.DataFrame(np.zeros((len(states),len(states))),index=pd.MultiIndex.from_frame(states),columns=pd.MultiIndex.from_frame(states))

    state_values = states.to_numpy(dtype=np.int8)
    state_tuples = [tuple(row) for row in state_values]
    state_pos = {state: idx for idx, state in enumerate(state_tuples)}
    nb_states = len(states)

    for tgt in states:
        tgt_pos = states.columns.get_loc(tgt)
        inpt, _ = mn.utils.T(adjmat, states, tgt)
        s = inpt.shape[1]
        inpt_idx = pd.MultiIndex.from_frame(inpt)
        f = mn.utils.MBF(s).loc[inpt_idx]
        for fi in f.columns:
            next_states = state_values.copy()
            next_states[:, tgt_pos] = f[fi].to_numpy()
            dest_idx = np.fromiter(
                (state_pos[tuple(row)] for row in next_states),
                dtype=np.int64,
                count=nb_states,
            )
            STG.to_numpy()[np.arange(nb_states), dest_idx] += 1
    return STG


def plot_STG(states, seed=0):
    STGraph = nx.from_pandas_adjacency(states, create_using=nx.DiGraph)
    STGraph = nx.relabel_nodes(
        STGraph,
        lambda x: str(x).replace('(', '').replace(')', '').replace(', ', '').replace(',', ''),
    )

    fig, ax = plt.subplots(figsize=(5, 5))
    pos = nx.spring_layout(STGraph, seed=seed)
    edges = list(STGraph.edges(data=True))
    weights = [d.get('weight', 1) for _, _, d in edges]
    max_weight = max(weights) if weights else 1
    edge_colors = [d.get('weight', 1) for _, _, d in edges]

    # nx.draw_networkx_nodes(STGraph, pos, ax=ax, node_size=700, node_color='skyblue', margins=0.1)
    nx.draw_networkx_labels(STGraph, pos, ax=ax, font_size=12, font_weight='bold')
    nx.draw_networkx_edges(
        STGraph,
        pos,
        ax=ax,
        edge_color=edge_colors,
        edge_cmap=plt.cm.Greys,
        edge_vmin=0,
        edge_vmax=max_weight,
        node_size=1000,
        arrowsize=10,
        connectionstyle='arc3,rad=0.2',
    )
    return fig, ax

#%%
STG_A = STGen(adjmat) 
#%%
plot_STG(STG_A)
#%%
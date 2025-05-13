#%%
import numpy as np
import pandas as pd
from itertools import combinations_with_replacement
#%%
n = 3
factors = [1,3,5]
#%%
n = 4
factors = [1,6,14,19]
#%%
df = pd.read_csv(f'../Output/Multi/{n}-node_1-stable_classes.csv')
# %%
uniq = pd.unique(df['n_params'])
# %%
def factor_combinations(num, factors, n):
    # Generate all possible products with replacement
    for combo in combinations_with_replacement(factors, r=n):
        if np.prod(combo) == num:
            yield combo
uniq_combos = {u: list(factor_combinations(u, factors, n)) for u in uniq}
print(uniq_combos)
# %%

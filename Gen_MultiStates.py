import os
import numpy as np

def multi_states(n, i):
    os.makedirs('Output/Multi', exist_ok=True)
    multi = np.empty((0,n), dtype=int)
    for j in range(0, i):
        mask = np.zeros(n, dtype=int)
        mask[j] = 1
        multi = np.vstack((multi, mask))
    np.savetxt(f'Output/Multi/{n}-node_{i}-stable_states.csv', multi, fmt='%d', delimiter=',')

for n in range(2,5):
    for i in range(1,n+1):
        multi_states(n,i)
    
    

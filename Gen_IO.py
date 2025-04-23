import os
import numpy as np

def gen_inps(n):
    # Generate all possible inputs
    inputs = np.array(np.meshgrid(*[[0, 1]]*n)).T.reshape(-1, n)
    return inputs

def input_pairs(inputs):
    inp_sum = np.sum(inputs, axis=1)
    # Choose pairs where left < right sum
    lower_sum = np.array(np.where(inp_sum[:, None] < inp_sum))
    # Compute a comparison matrix where each element (i,j) is True if all elements of inputs[i] <= inputs[j]
    comparison = np.all(inputs[lower_sum[0]] <= inputs[lower_sum[1]], axis=1)
    # Select the indices of lower sum pairs where the comparison is True
    inp_pair = lower_sum[:, comparison]
    return inp_pair

def process_function(index, len_inputs):
    # Convert index to binary representation and make it an array
    return np.fromiter(np.binary_repr(index, width=len_inputs), dtype=int)

def is_monotonic(func, inp_pair):
    # Check if func(b1) <= func(b2)
    return (func[inp_pair[0]] <= func[inp_pair[1]]).all()

def return_func_if_monotonic(func_index, inputs, inp_pair):
    func = process_function(func_index, len(inputs))
    if is_monotonic(func, inp_pair):
        return func

def saveio(n):
    inputs = gen_inps(n)
    inp_pair = input_pairs(inputs)
    all_funcs = range(2**len(inputs))
    os.makedirs('Output/IO', exist_ok=True)
    np.savetxt(f'Output/IO/Inputs_B{n}.csv', inputs, delimiter=',', fmt='%d')
    monotonic_funcs = list(map(lambda func_index: return_func_if_monotonic(func_index, inputs, inp_pair), all_funcs))
    # Remove None values from monotonic_funcs
    monotonic_funcs = [x for x in monotonic_funcs if x is not None]
    # Save the monotonic functions
    monotonic_funcs = np.array(monotonic_funcs)
    np.savetxt(f'Output/IO/MBF_B{n}.csv', monotonic_funcs, delimiter=',', fmt='%d')

# Iterate over Number of boolean inputs B^n
for n in range(1,5):
    saveio(n)
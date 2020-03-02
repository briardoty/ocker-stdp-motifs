from brian2 import *
import numpy as np

def compute_motif_stats(network_group, synapses):
    """
    
    """
    # Create a matrix to store the weights and fill it with NaN
    N = len(network_group)
    W = np.zeros((N, N))

    # Insert the values from the Synapses object
    W[synapses.i[:], synapses.j[:]] = synapses.w[:]

    # motif stats...
    p = W.sum() / N**2

    q_div = 0
    for i in range(N):
        for j in range(N):
            for k in range(N):
                q_div += W[i,k] * W[j,k]

    q_div = (q_div - p**2) / N**3
    return (p, q_div)

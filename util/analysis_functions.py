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

    q_div = q_con = q_ch = q_rec = 0
    for i in range(N):
        for j in range(N):
            q_rec += W[i,j] * W[j,i]
            for k in range(N):
                q_div += W[i,k] * W[j,k]
                q_con += W[i,k] * W[i,j]
                q_ch += W[i,j] * W[j,k]


    q_div = (q_div / N**3) - p**2
    q_con = (q_con / N**3) - p**2
    q_ch = (q_ch / N**3) - p**2
    q_rec = (q_rec / N**3) - p**2
    return (p, q_div, q_con, q_ch, q_rec)

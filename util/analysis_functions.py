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
    p = sum(W) / N**2
    q_div = sum(W * W.transpose()) / N**3 - p**2
    q_con = sum(W.transpose() * W) / N**3 - p**2
    q_ch = sum(W * W)/ N**3 - p**2
    q_rec = sum(np.multiply(W,W.transpose())) / N**2 - p**2

    return (p, q_div, q_con, q_ch, q_rec)

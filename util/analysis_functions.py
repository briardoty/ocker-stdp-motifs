from brian2 import *
import numpy as np

def compute_motif_stats_from_matrix(W, N):
    """
    Compute motif stats based on weight matrix
    Args:
        W (N x N matrix): weight matrix
        N (int): number of neurons
    Returns:
        motif_stats: 5-tuple of motif stats like (p, q_div, q_con, q_ch, q_rec)
    """
    # motif stats...
    p = sum(W) / N**2
    q_div = sum(W * W.transpose()) / N**3 - p**2
    q_con = sum(W.transpose() * W) / N**3 - p**2
    q_ch = sum(W * W)/ N**3 - p**2
    q_rec = sum(np.multiply(W,W.transpose())) / N**2 - p**2

    return (p, q_div, q_con, q_ch, q_rec)

def compute_motif_stats(network_group, synapses):
    """
    Compute motif statistics for network
    Args:
        network_group (NeuronGroup): Brian2 neurons in network
        synapses (Synapses): Brian2 synapses in network
    Returns:
        motif_stats: 5-tuple of motif stats like (p, q_div, q_con, q_ch, q_rec)
    """
    # Create a matrix to store the weights and fill it with NaN
    N = len(network_group)
    W = np.zeros((N, N))

    # Insert the values from the Synapses object
    W[synapses.i[:], synapses.j[:]] = synapses.w[:]

    return compute_motif_stats_from_matrix(W, N)

def get_motif_stats_in_time(w_mon, synapses, n_samples, N):
    """
    Computes motif statistics at 
    Args:
        w_mon (StateMonitor): Brian2 synaptic weight monitor
        synapses (Synapses): Brian2 synapses in network
        n_samples (int): number of time samples to take motif stats at
        N (int): number of neurons
    Returns:
        motif_stats_arr (array): array of motif_stats tuples
    """
    t_i_arr = np.linspace(0, len(w_mon.t)-1, n_samples, True, False, int)

    W = np.zeros((N, N, n_samples))
    W[synapses.i[:], synapses.j[:], :] = w_mon.w[:,t_i_arr]

    motif_stats_arr = [compute_motif_stats_from_matrix(W[:,:,i], N) for i in range(len(t_i_arr))]
    return motif_stats_arr

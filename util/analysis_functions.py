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
    # Create a matrix to store the weights
    N = len(network_group)
    W = np.zeros((N, N))

    # Insert the values from the Synapses object
    W[synapses.i[:], synapses.j[:]] = synapses.w[:]

    return compute_motif_stats_from_matrix(W, N)

def compute_p0(network_group, synapses):
    """
    Compute initial connection density of network
    Args:
        network_group (NeuronGroup): Brian2 neurons in network
        synapses (Synapses): Brian2 synapses in network
    Returns:
        p0 (number): initial connection density
    """
    # Create a matrix to store the weights
    N = len(network_group)
    adj = np.zeros((N, N))

    # Insert the values from the Synapses object
    adj[synapses.i[:], synapses.j[:]] = 1
    p0 = sum(adj) / N**2

    return p0

def get_motif_stats_in_time(w_mon, synapses, N):
    """
    Computes motif statistics at 
    Args:
        w_mon (StateMonitor): Brian2 synaptic weight monitor
        synapses (Synapses): Brian2 synapses in network
        N (int): number of neurons
    Returns:
        motif_stats_mat (len(w_mon.t) x 5): matrix of motif_stats
    """
    W = np.zeros((N, N, len(w_mon.t)))
    W[synapses.i[:], synapses.j[:], :] = w_mon.w[:,:]

    motif_stats_mat = np.zeros((len(w_mon.t), 5))

    for i in range(len(w_mon.t)):
        motif_stats_mat[i,:] = compute_motif_stats_from_matrix(W[:,:,i], N)

    return motif_stats_mat

def get_motif_stats_in_time2(w_mon_exc, w_mon_inh, synapses_exc, synapses_inh, N_exc, N_inh):
    """
    Computes motif statistics at 
    Args:
        w_mon (StateMonitor): Brian2 synaptic weight monitor
        synapses (Synapses): Brian2 synapses in network
        N (int): number of neurons
    Returns:
        motif_stats_mat (len(w_mon.t) x 5): matrix of motif_stats
    """
    N = N_exc + N_inh
    len_t = max(len(w_mon_exc.t), len(w_mon_inh.t))
    
    W = np.zeros((N, N, len_t))
    W[synapses_exc.i[:], synapses_exc.j[:], :] = w_mon_exc.w[:,:]
    W[synapses_inh.i[:] + N_exc, synapses_inh.j[:], :] = w_mon_inh.w[:,:]

    motif_stats_mat = np.zeros((len_t, 5))

    for i in range(len_t):
        motif_stats_mat[i,:] = compute_motif_stats_from_matrix(W[:,:,i], N)

    return motif_stats_mat
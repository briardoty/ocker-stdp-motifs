from brian2 import *
import numpy as np

def compute_all_motif_stats_from_matrix(W_EE, W_II, W_EI, W_IE, N, p0):
    """
    Compute motif stats based on weight matrix
    Args:
        W (N x N matrix): weight matrix
        N (int): number of neurons
    Returns:
        motif_stats: 5-tuple of motif stats like (p, q_div, q_con, q_ch, q_rec)
    """
    # motif stats...
    p_EE = sum(W_EE) / N**2
    p_EI = sum(W_EI) / N**2
    p = (sum(W_EE) + sum(W_EI) + sum(W_IE) + sum(W_II)) / N**2
    
    if not (p0):
        p0 = p
    
    q_div_EE = sum(np.matmul(W_EE, W_EE.transpose())) / N**3 - p_EE**2 #p0**2
    q_div_IEI = sum(np.matmul(W_EI, W_EI.transpose())) / N**3 - p_EI**2 # p0**2
    q_div_EEI = sum(np.matmul(W_EI, W_EE.transpose())) / N**3 - p_EE*p_EI #p0**2 # 0

    q_con_EE = sum(np.matmul(W_EE.transpose(), W_EE)) / N**3 - p_EE**2 #p0**2
    q_con_EIE = sum(np.matmul(W_EI.transpose(), W_EI)) / N**3 - p_EI**2 #p0**2    
    q_con_EEI = sum(np.matmul(W_EE.transpose(), W_IE)) / N**3 - p0**2 # 0
    
    q_ch_EE = sum(np.matmul(W_EE, W_EE))/ N**3 - p_EE**2 #p0**2
    q_ch_IEE = sum(np.matmul(W_IE, W_EE))/ N**3 - p0**2
    q_ch_EIE = sum(np.matmul(W_EI, W_IE))/ N**3 - p0**2
    q_ch_EEI = sum(np.matmul(W_EE, W_EI))/ N**3 - p_EE*p_EI #p0**2
    
    q_rec_EE = sum(np.multiply(W_EE, W_EE.transpose())) / N**2 - p_EE**2 #p0**2 # Element wise
    q_rec_EI = sum(np.multiply(W_EI, W_IE.transpose())) / N**2 - p0**2 # Element wise

    return (-p**2, p_EE, p_EI, q_div_EE, q_div_IEI, q_div_EEI, q_con_EE, q_con_EIE, q_con_EEI, q_ch_EE, 
            q_ch_IEE, q_ch_EIE, q_ch_EEI, q_rec_EE, q_rec_EI)

def compute_motif_stats_from_matrix(W, N, p0):
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
    
    if not (p0):
        p0 = p
        
    q_div = sum(np.matmul(W, W.transpose())) / N**3 - p0**2
    q_con = sum(np.matmul(W.transpose(), W)) / N**3 - p0**2
    q_ch = sum(np.matmul(W, W))/ N**3 - p0**2
    q_rec = sum(np.multiply(W,W.transpose())) / N**2 - p0**2 # Element wise

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

def get_motif_stats_in_time(w_mon, synapses, N, use_p0=True):
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

    if use_p0:
        p0 = sum(W[:,:,0]) / N**2
    else:
        p0 = False
        
    motif_stats_mat = np.zeros((len(w_mon.t), 5))

    for i in range(len(w_mon.t)):
        motif_stats_mat[i,:] = compute_motif_stats_from_matrix(W[:,:,i], N, p0=p0)

    return motif_stats_mat

def get_motif_stats_in_time2(w_mon_exc, w_mon_inh, synapses_exc, synapses_inh, N_exc, N_inh, use_p0=True):
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

    if use_p0:
        p0 = sum(W[:,:,0]) / N**2
    else:
        p0 = False
        
    motif_stats_mat = np.zeros((len_t, 5))

    for i in range(len_t):
        motif_stats_mat[i,:] = compute_motif_stats_from_matrix(W[:,:,i], N, p0=p0)

    return motif_stats_mat

def get_all_motif_stats_in_time2(w_mon_exc, w_mon_inh, synapses_exc, synapses_inh, N_exc, N_inh, use_p0=True):
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

    W_EE = W.copy()
    W_EE[N_exc:, :, :] = 0
    W_EE[:, N_exc:, :] = 0

    W_II = W.copy()
    W_II[:N_exc, :, :] = 0
    W_II[:, :N_exc, :] = 0

    W_IE = W.copy()
    W_IE[:N_exc, :, :] = 0
    W_IE[:, N_exc:, :] = 0

    W_EI = W.copy()
    W_EI[N_exc:, :, :] = 0
    W_EI[:, :N_exc, :] = 0
    motif_stats_mat = np.zeros((len_t, 15))
    
    if use_p0:
        p0 = sum(W[:,:,0]) / N**2
    else:
        p0 = False

    for i in range(len_t):
        motif_stats_mat[i,:] = compute_all_motif_stats_from_matrix(W_EE[:,:,i], W_II[:,:,i], W_EI[:,:,i], W_IE[:,:,i], N, p0)

    return motif_stats_mat
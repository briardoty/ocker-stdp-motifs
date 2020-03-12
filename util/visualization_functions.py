from brian2 import *
from util.analysis_functions import *

def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10, 4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0, 1], [i, j], '-k')
    xticks([0, 1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    plot(S.i, S.j, '.k')
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')
    
def visualize_stdp(A_pre, tau_pre, A_post, tau_post):
    delta_t = linspace(-100, 100, 100)*ms
    W = where(delta_t>0, A_pre*exp(-delta_t/tau_pre), A_post*exp(delta_t/tau_post))
    plot(delta_t/ms, W)
    xlabel(r'$\Delta t$ (ms)')
    ylabel('W')
    axhline(0, ls='-', c='k')

def plot_v(v_mon, sp_mon_exc, i, include_spikes=False):
    """
    Plot voltage trace for the given neuron with optional spikes
    Args:
        v_mon (StateMonitor): Brian2 voltage monitor
        sp_mon_exc: Brian2 neuron spike monitor for excitatory neurons
        i (int): neuron index
        include_spikes (bool): optional param to plot spike times
    """
    plt.figure(figsize=(10, 5))
    plot(v_mon.t/ms, v_mon.v[i]/mV)

    xlabel('Time (ms)')
    ylabel('mV')

    if (not include_spikes):
        return

    n_i_spike_train = sp_mon_exc.spike_trains()[i]
    for t in n_i_spike_train:
        axvline(t/ms, ls='--', c='C1', lw=3)

def plot_spike_trains(sp_mon_exc):
    """
    Plot spike trains for all neurons in given monitor
    Args:
        sp_mon_exc: Brian2 neuron spike monitor for excitatory neurons
    """
    plt.figure(figsize=(10, 5))
    plot(sp_mon_exc.t/ms, sp_mon_exc.i, '|r')
    xlabel('Time (ms)')
    ylabel('Neuron')

def plot_avg_syn_weight(w_mon, w_max):
    """
    Plot average synaptic weight over time
    Args:
        w_mon (StateMonitor): Brian2 synaptic weight monitor
        w_max (number): max synaptic weight per STDP rule
    """
    avg_w_e = w_mon.w.mean(axis=0)
    plot(w_mon.t/second, avg_w_e/w_max)
    title('Excitatory Neuron Average Weight')
    xlabel('Time (s)')
    ylabel('Average Weight / gmax')
    plt.show()

def plot_motif_dynamics(w_mon, synapses, N, save_fig=False):
    """
    Plot motif dynamics a la figure 7 from Ocker et al 2015
    Args:
        w_mon (StateMonitor): Brian2 synaptic weight monitor
        synapses (Synapses): Brian2 synapses in network
        N (int): number of neurons
        save_fig (bool): optional flag to output figure image
    """
    motif_names = ["p", "q_div", "q_con", "q_ch", "q_rec"]
    motif_stats_mat = get_motif_stats_in_time(w_mon, synapses, N)

    fig, axes = plt.subplots(5, figsize=(5, 10))

    plt.xlabel("Time (s)")
    fig.suptitle("Motif dynamics: N=" + str(N))
    for i in range(5):
        ax = axes[i]
        ax.plot(w_mon.t, motif_stats_mat[:, i])
        ax.set_ylabel(motif_names[i])

    if not save_fig:
        return

    now = str(time.time())
    name = "results/motifs_N=" + str(N) + "_t=" + str(w_mon.t[-1]) + "_" + now + ".png"
    plt.savefig(name, dpi=300, bbox_inches='tight')

def plot_motif_dynamics2(w_mon_exc, w_mon_inh, synapses_exc, synapses_inh, N_exc, N_inh, save_fig=False):
    """
    Plot motif dynamics a la figure 7 from Ocker et al 2015
    Args:
        w_mon (StateMonitor): Brian2 synaptic weight monitor
        synapses (Synapses): Brian2 synapses in network
        N (int): number of neurons
        save_fig (bool): optional flag to output figure image
    """
    motif_names = ["p", "q_div", "q_con", "q_ch", "q_rec"]
    motif_stats_mat = get_motif_stats_in_time2(w_mon_exc, w_mon_inh, synapses_exc, synapses_inh, N_exc, N_inh)

    fig, axes = plt.subplots(5, figsize=(5, 10))

    plt.xlabel("Time (s)")
    fig.suptitle("Motif dynamics: N_exc=" + str(N_exc) + "; N_inh=" + str(N_inh))
    for i in range(5):
        ax = axes[i]
        ax.plot(w_mon_exc.t, motif_stats_mat[:, i])
        ax.set_ylabel(motif_names[i])

    if not save_fig:
        return

    now = str(time.time())
    name = "results/motifs_N_exc=" + str(N_exc) + "_N_inh=" + str(N_inh) + "_t=" + str(w_mon_exc.t[-1]) + "_" + now + ".png"
    plt.savefig(name, dpi=300, bbox_inches='tight')
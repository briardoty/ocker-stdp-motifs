from brian2 import *

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

def plot_motif_dynamics(w_mon):
    """
    Plot motif dynamics a la figure 7 from Ocker et al 2015
    Args:
        w_mon (StateMonitor): Brian2 synaptic weight monitor
    """
    t = np.linspace(0, len(w_mon.t), 100, True, False, int)

    motif_stats = np.zeros(())


    return


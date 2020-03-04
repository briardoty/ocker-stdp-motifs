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
    """
    plt.figure(figsize=(10, 5))
    plot(sp_mon_exc.t/ms, sp_mon_exc.i, '|r')
    xlabel('Time (ms)')
    ylabel('Neuron')

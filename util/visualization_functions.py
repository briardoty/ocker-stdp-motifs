from brian2 import *
from util.analysis_functions import *

import brian2 as b2
import matplotlib.pyplot as plt
import numpy

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

def plot_motif_dynamics(w_mon, synapses, N, use_p0=True, save_fig=False):
    """
    Plot motif dynamics a la figure 7 from Ocker et al 2015
    Args:
        w_mon (StateMonitor): Brian2 synaptic weight monitor
        synapses (Synapses): Brian2 synapses in network
        N (int): number of neurons
        save_fig (bool): optional flag to output figure image
    """
    motif_names = ["p", "q_div", "q_con", "q_ch", "q_rec"]
    motif_stats_mat = get_motif_stats_in_time(w_mon, synapses, N, use_p0=use_p0)

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

def plot_motif_dynamics2(w_mon_exc, w_mon_inh, synapses_exc, synapses_inh, N_exc, N_inh, use_p0=True, save_fig=False):
    """
    Plot motif dynamics a la figure 7 from Ocker et al 2015
    Args:
        w_mon (StateMonitor): Brian2 synaptic weight monitor
        synapses (Synapses): Brian2 synapses in network
        N (int): number of neurons
        save_fig (bool): optional flag to output figure image
    """
    motif_names = ["p", "q_div", "q_con", "q_ch", "q_rec"]
    motif_stats_mat = get_motif_stats_in_time2(w_mon_exc, w_mon_inh, synapses_exc, synapses_inh, N_exc, N_inh, use_p0=use_p0)

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
    
def plot_all_motif_dynamics2(w_mon_exc, w_mon_inh, synapses_exc, synapses_inh, N_exc, N_inh, use_p0=True, save_fig=False):
    """
    Plot motif dynamics a la figure 7 from Ocker et al 2015
    Args:
        w_mon (StateMonitor): Brian2 synaptic weight monitor
        synapses (Synapses): Brian2 synapses in network
        N (int): number of neurons
        save_fig (bool): optional flag to output figure image
    """
    motif_names = ["-p**2", "p_EE", "p_EI", "q_div_EE", "q_div_IEI", "q_div_EEI", "q_con_EE", "q_con_EIE", "q_con_EEI", "q_ch_EE",
"q_ch_IEE", "q_ch_EIE", "q_ch_EEI", "q_rec_EE", "q_rec_EI"]
    motif_stats_mat = get_all_motif_stats_in_time2(w_mon_exc, w_mon_inh, synapses_exc, synapses_inh, N_exc, N_inh, use_p0=use_p0)

    fig, axes = plt.subplots(15, figsize=(5, 20))

    plt.xlabel("Time (s)")
    fig.suptitle("Motif dynamics: N_exc=" + str(N_exc) + "; N_inh=" + str(N_inh))
    for i in range(15):
        ax = axes[i]
        ax.plot(w_mon_exc.t, motif_stats_mat[:, i])
        ax.set_ylabel(motif_names[i])

    if not save_fig:
        return

    now = str(time.time())
    name = "results/motifs_N_exc=" + str(N_exc) + "_N_inh=" + str(N_inh) + "_t=" + str(w_mon_exc.t[-1]) + "_" + now + ".png"
    plt.savefig(name, dpi=300, bbox_inches='tight')

def plot_network_activity(rate_monitor, spike_monitor, weight_monitor, synapse_idx_list,
                          t_min=None, t_max=None, N_highlighted_spiketrains=3, avg_window_width=1.0 * b2.ms,
                          sup_title=None, figure_size=(10, 4)):
    """
    Visualizes the results of a network simulation: spike-train, population activity and weight-traces.

    Args:
        rate_monitor (PopulationRateMonitor): rate of the population
        spike_monitor (SpikeMonitor): spike trains of individual neurons
        weight_monitor (StateMonitor): optional. voltage traces of some (same as in spike_train_idx_list) neurons
        synapse_idx_list (list): optional. A list of synapse indices whose weight changes are plotted.
            If no list is provided, all (up to 500) spike-trains in the spike_monitor are plotted. If None, the
            the list in voltage_monitor.record is used.
        t_min (Quantity): optional. lower bound of the plotted time interval.
            if t_min is None, it is set to the larger of [0ms, (t_max - 100ms)]
        t_max (Quantity): optional. upper bound of the plotted time interval.
            if t_max is None, it is set to the timestamp of the last spike in
        N_highlighted_spiketrains (int): optional. Number of spike trains visually highlighted, defaults to 3
            If N_highlighted_spiketrains==0 and voltage_monitor is not None, then all voltage traces of
            the voltage_monitor are plotted. Otherwise N_highlighted_spiketrains voltage traces are plotted.
        avg_window_width (Quantity): optional. Before plotting the population rate (PopulationRateMonitor), the rate
            is smoothed using a window of width = avg_window_width. Defaults is 1.0ms
        sup_title (String): figure suptitle. Default is None.
        figure_size (tuple): (width,height) tuple passed to pyplot's figsize parameter.

    Returns:
        Figure: The whole figure
        Axes: Top panel, Raster plot
        Axes: Middle panel, population activity
        Axes: Bottom panel, weight traces. None if no weight monitor is provided.
    """

    assert isinstance(rate_monitor, b2.PopulationRateMonitor), \
        "rate_monitor  is not of type PopulationRateMonitor"
    assert isinstance(spike_monitor, b2.SpikeMonitor), \
        "spike_monitor is not of type SpikeMonitor"
    assert isinstance(weight_monitor, b2.StateMonitor), \
        "weight_monitor is not of type StateMonitor"
    assert isinstance(synapse_idx_list, list), \
        "synapse_idx_list is not of type list"

    # get a reasonable default interval
    if t_max is None:
        t_max = max(rate_monitor.t / b2.ms)
    else:
        t_max = t_max / b2.ms
    if t_min is None:
        t_min = max(0., t_max - 100.)  # if none, plot at most the last 100ms
    else:
        t_min = t_min / b2.ms

    fig = None
    ax_raster = None
    ax_rate = None
    ax_weight = None
    
    fig, (ax_raster, ax_rate, ax_weight) = plt.subplots(3, 1, sharex=True, figsize=figure_size)

    # nested helpers to plot the parts, note that they use parameters defined outside.
    def get_spike_train_ts_indices(spike_train):
        """
        Helper. Extracts the spikes within the time window from the spike train
        """
        ts = spike_train/b2.ms
        # spike_within_time_window = (ts >= t_min) & (ts <= t_max)
        # idx_spikes = numpy.where(spike_within_time_window)
        idx_spikes = (ts >= t_min) & (ts <= t_max)
        ts_spikes = ts[idx_spikes]
        return idx_spikes, ts_spikes

    def plot_raster():
        """
        Helper. Plots the spike trains of the spikes in spike_train_idx_list
        """
        neuron_counter = 0
        for neuron_index in synapse_idx_list:
            idx_spikes, ts_spikes = get_spike_train_ts_indices(all_spike_trains[neuron_index])
            ax_raster.scatter(ts_spikes, neuron_counter * numpy.ones(ts_spikes.shape),
                              marker=".", c="k", s=15, lw=0)
            neuron_counter += 1
        ax_raster.set_ylim([0, neuron_counter])

    def highlight_raster(neuron_idxs):
        """
        Helper. Highlights three spike trains
        """
        for i in range(len(neuron_idxs)):
            color = "r" if i == 0 else "k"
            raster_plot_index = neuron_idxs[i]
            population_index = synapse_idx_list[raster_plot_index]
            idx_spikes, ts_spikes = get_spike_train_ts_indices(all_spike_trains[population_index])
            ax_raster.axhline(y=raster_plot_index, linewidth=.5, linestyle="-", color=[.9, .9, .9])
            ax_raster.scatter(
                ts_spikes, raster_plot_index * numpy.ones(ts_spikes.shape),
                marker=".", c=color, s=144, lw=0)
        ax_raster.set_ylabel("neuron #")
        ax_raster.set_title("Raster Plot", fontsize=10)

    def plot_population_activity(window_width=0.5*b2.ms):
        """
        Helper. Plots the population rate and a mean
        """
        ts = rate_monitor.t / b2.ms
        idx_rate = (ts >= t_min) & (ts <= t_max)
        # ax_rate.plot(ts[idx_rate],rate_monitor.rate[idx_rate]/b2.Hz, ".k", markersize=2)
        smoothed_rates = rate_monitor.smooth_rate(window="flat", width=window_width)/b2.Hz
        ax_rate.plot(ts[idx_rate], smoothed_rates[idx_rate])
        ax_rate.set_ylabel("A(t) [Hz]")
        ax_rate.set_title("Population Activity", fontsize=10)

    def plot_weights(weights_i):
        """
        Helper. Plots three weight traces
        """
        ts = weight_monitor.t/b2.ms
        idx_weight = (ts >= t_min) & (ts <= t_max)
        for i in range(len(weights_i)):
            color = "r" if i == 0 else ".7"
            raster_plot_index = weights_i[i]
            population_index = synapse_idx_list[raster_plot_index]
            ax_weight.plot(
                ts[idx_weight], weight_monitor[population_index].w[idx_weight]/b2.mV,
                c=color, lw=1.)
            ax_weight.set_ylabel("Weight [$A m^{-2}$]")
            ax_weight.set_title("Synaptic Weights", fontsize=10)
        
    all_spike_trains = spike_monitor.spike_trains()
    plot_raster()
    plot_population_activity(avg_window_width)
    nr_neurons = len(synapse_idx_list)
    highlighted_neurons_i = []  # default to an empty list.
    
    if N_highlighted_spiketrains > 0:
        fract = numpy.linspace(0, 1, N_highlighted_spiketrains + 2)[1:-1]
        highlighted_neurons_i = [int(nr_neurons * v) for v in fract]
        highlight_raster(highlighted_neurons_i)

    if N_highlighted_spiketrains == 0:
        traces_i = range(nr_neurons)
    else:
        traces_i = highlighted_neurons_i
    plot_weights(traces_i)

    plt.xlabel("t [ms]")

    if sup_title is not None:
        plt.suptitle(sup_title)

    return fig, ax_raster, ax_rate, ax_weight
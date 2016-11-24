import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../')
from graphs.my_graph import set_plot

def get_stimulus_responses(filename, window=[-100, 400]):
    params = get_metadata(filename)
    t, VEC = BIN_load(filename)    
    delays = np.loadtxt(filename.replace('data.bin', 'DELAYS.TXT'))
    commands = np.loadtxt(filename.replace('data.bin', 'COMMANDS.TXT'))
    stim_flag = np.loadtxt(filename.replace('data.bin', 'STIM_FLAG.TXT'))
    up_transitions = np.loadtxt(filename.replace('data.bin', 'UP_TRANSITIONS.TXT'))
    down_transitions = np.loadtxt(filename.replace('data.bin', 'DOWN_TRANSITIONS.TXT'))
    durations = np.loadtxt(filename.replace('data.bin', 'DURATIONS.TXT'))
    if params['flag_for_state_stimulation']=='1':
        test_conditions = np.arange(len(delays))[(stim_flag==1) & (up_transitions>0.)]
        ctrl_conditions = np.arange(len(delays))[(stim_flag==0) & (up_transitions>0.)]
        t_tests = up_transitions[test_conditions]
        t_ctrls = up_transitions[ctrl_conditions]
    elif params['flag_for_state_stimulation']=='2':
        test_conditions = np.arange(len(delays))[(stim_flag==1) & (down_transitions>0.)]
        ctrl_conditions = np.arange(len(delays))[(stim_flag==0) & (down_transitions>0.)]
        t_tests = down_transitions[test_conditions]
        t_ctrls = down_transitions[ctrl_conditions]

    t_window = np.linspace(window[0], window[1],\
                           int(1e-3*(window[1]-window[0])/(t[1]-t[0])))
    TEST_TRACES, CTRL_TRACES = [], []
    TEST_COND, CTRL_COND = [[],[],[]], [[],[],[]]
    for tt, ctrl_cond in zip(t_ctrls, ctrl_conditions):
        vv = VEC[0][(1e3*t>=tt+window[0]) &(1e3*t<=tt+window[1])]
        if len(vv)==len(t_window):
            CTRL_TRACES.append(vv)
            CTRL_COND[0].append(delays[ctrl_cond])
            CTRL_COND[1].append(durations[ctrl_cond])
            CTRL_COND[2].append(commands[ctrl_cond])
    for tt, test_cond in zip(t_tests, test_conditions):
        vv = VEC[0][(1e3*t>=tt+window[0]) &(1e3*t<=tt+window[1])]
        if len(vv)==len(t_window):
            TEST_TRACES.append(vv)
            TEST_COND[0].append(delays[test_cond])
            TEST_COND[1].append(durations[test_cond])
            TEST_COND[2].append(commands[test_cond])
    return t_window, TEST_TRACES, CTRL_TRACES, TEST_COND, CTRL_COND, params


def fig_with_sample_traces(t_window, TEST_TRACES, CTRL_TRACES, delay, duration,\
                           threshold=-30, color='b'):
    # then fig with all traces
    fig, ax = plt.subplots(1, figsize=(5,3.5))
    ax.set_title('delay='+str(delay)+'ms, duration='+str(duration)+'ms, n='+\
                 str(len(TEST_TRACES))+' trials',fontsize=12)
    plt.subplots_adjust(left=.2, bottom=.25)
    for v in CTRL_TRACES[:10]:
        ax.plot(t_window, v, 'k', lw=.5)
    ax.plot(t_window, CTRL_TRACES[-1], 'k',\
            label='blank trials \n (10 samples)', lw=.5)
    for v in TEST_TRACES[:10]:
        plt.plot(t_window, v, color, lw=.5)
    ax.plot(t_window, TEST_TRACES[-1], color,\
            label='test trials \n (10 samples)', lw=.5)
    ax.legend(prop={'size':'x-small'}, loc='best', frameon=False)
    set_plot(ax, ylabel='$V_m$ (mV)', xlabel='delay from state onset (ms)')
    ax.fill_between([delay, delay+duration],\
                    ax.get_ylim()[0]*np.ones(2), ax.get_ylim()[1]*np.ones(2),\
                    color=color, alpha=.2)
    return fig

def fig_with_average_trace(t_window, TEST_TRACES, CTRL_TRACES, delay, duration,\
                           threshold=-30, color='b'):
    # then fig with averages
    fig, ax = plt.subplots(1, figsize=(5,3.5))
    ax.set_title('delay='+str(delay)+'ms, duration='+str(duration)+'ms, n='+\
                 str(len(TEST_TRACES))+' trials',fontsize=12)
    plt.subplots_adjust(left=.2, bottom=.25)
    CTRL_TRACES = np.array(CTRL_TRACES)
    CTRL_TRACES[CTRL_TRACES>threshold] = threshold
    TEST_TRACES = np.array(TEST_TRACES)
    TEST_TRACES[TEST_TRACES>threshold] = threshold
    ax.plot(t_window, CTRL_TRACES.mean(axis=0), 'k', lw=2, label='blank trials')
    ax.fill_between(t_window,\
                    CTRL_TRACES.mean(axis=0)-CTRL_TRACES.std(axis=0),\
                    CTRL_TRACES.mean(axis=0)+CTRL_TRACES.std(axis=0),
                    color='lightgray')
    ax.plot(t_window,\
                    CTRL_TRACES.mean(axis=0)-CTRL_TRACES.std(axis=0),\
                    color='k', lw=.5)
    ax.plot(t_window,\
                    CTRL_TRACES.mean(axis=0)+CTRL_TRACES.std(axis=0),
                    color='k', lw=.5)
    ax.plot(t_window, TEST_TRACES.mean(axis=0), color, lw=2, label='test trials')
    ax.plot(t_window,\
            TEST_TRACES.mean(axis=0)+TEST_TRACES.std(axis=0),
            color=color, lw=.5)
    ax.plot(t_window,\
            TEST_TRACES.mean(axis=0)-TEST_TRACES.std(axis=0),\
            color=color, lw=.5)
    ax.fill_between(t_window,\
                    TEST_TRACES.mean(axis=0)-TEST_TRACES.std(axis=0),\
                    TEST_TRACES.mean(axis=0)+TEST_TRACES.std(axis=0),
                    color=color, alpha=.3)
    ax.legend(prop={'size':'small'}, loc='best', frameon=False)
    set_plot(ax, ylabel='$V_m$ (mV)', xlabel='delay from state onset (ms)')
    ax.fill_between([delay, delay+duration],\
                    ax.get_ylim()[0]*np.ones(2), ax.get_ylim()[1]*np.ones(2),\
                    color=color, alpha=.2)
    return fig
    
def make_fig(t_window, TEST_TRACES, CTRL_TRACES, TEST_COND, CTRL_COND, params,\
             threshold=-30, color='b'):
    FIGS = []
    delays, durations = np.unique(TEST_COND[0]), np.unique(TEST_COND[1])
    for delay in delays:
        for duration in durations:
            i0 = np.argwhere((TEST_COND[0]==delay) & (TEST_COND[1]==duration)).flatten()
            #  ctrl trials (random pick !!) as the same number than test_trials
            i1 = np.random.choice(np.arange(len(CTRL_TRACES)), len(i0), replace=False)
            fig1 = fig_with_sample_traces(t_window,\
               np.array(TEST_TRACES)[i0], np.array(CTRL_TRACES)[i1], delay, duration,\
                                          color=color, threshold=threshold)
            fig2 = fig_with_average_trace(t_window,\
               np.array(TEST_TRACES)[i0], np.array(CTRL_TRACES)[i1], delay, duration,\
                                          color=color, threshold=threshold)
            FIGS = FIGS+[fig1, fig2]
    return FIGS

def plot_analysis(main):
    return make_fig(*get_stimulus_responses(main.filename))

### Response to current Pulses

def v_resp(t, El, Tm, Gl, t0=0., t1=1., I0=1.):
    v = np.ones(len(t))*El
    if t0>=t1:
        print('/!\  t0 and t1 need to be ordered !')
    v[t>=t0] = El+I0/Gl*(1-np.exp(-(t[t>=t0]-t0)/Tm))
    v[t>=t1] = El+I0/Gl*(np.exp(t1/Tm)-np.exp(t0/Tm))*np.exp(-t[t>=t1]/Tm)
    return v

from scipy.optimize import curve_fit

def fit_membrane_prop(t, mean_resp, params):
    def func(t, El, Cm, Gl):
        return v_resp(t, El, Cm, Gl, t0=float(params['CMD_delay']),\
                      t1=float(params['CMD_dur'])+float(params['CMD_delay']),\
                      I0=float(params['current_pulse']))
    func(t, -70., 10., 1e-3)
    [El, Cm, Gl], pcov = curve_fit(func, t, mean_resp)
    return El, Cm, Gl, func

def fig_with_current_pulse_analysis(t_window, TEST_TRACES, CTRL_TRACES,\
                                    delay, duration, params,\
                                    threshold=-30, color='k'):
    CTRL_TRACES = np.array(CTRL_TRACES)
    CTRL_TRACES[CTRL_TRACES>threshold] = threshold
    # then fig with all traces
    fig, ax = plt.subplots(1, figsize=(5,3.5))
    ax.set_title('n='+str(len(CTRL_TRACES))+' trials',fontsize=12)
    plt.subplots_adjust(left=.2, bottom=.25)
    for v in CTRL_TRACES:
        plt.plot(t_window, v, color, lw=.2)
    ax.legend(prop={'size':'x-small'}, loc='best', frameon=False)
    ax.plot(t_window, CTRL_TRACES.mean(axis=0), 'k', lw=2, label='blank trials')
    ax.fill_between(t_window,\
                    CTRL_TRACES.mean(axis=0)-CTRL_TRACES.std(axis=0),\
                    CTRL_TRACES.mean(axis=0)+CTRL_TRACES.std(axis=0),
                    color='lightgray')
    ax.plot(t_window,\
                    CTRL_TRACES.mean(axis=0)-CTRL_TRACES.std(axis=0),\
                    color='k', lw=.5)
    ax.plot(t_window,\
                    CTRL_TRACES.mean(axis=0)+CTRL_TRACES.std(axis=0),
                    color='k', lw=.5)
    ## now fitting
    tcond = (t_window>float(params['CMD_delay'])-10.) & (t_window<float(params['CMD_delay'])+float(params['CMD_dur']))
    params = get_metadata(filename)
    El, Tm, Gl, func = fit_membrane_prop(t_window[tcond],\
                                         CTRL_TRACES.mean(axis=0)[tcond], params)
    ax.plot(t_window[tcond], func(t_window[tcond], El, Tm, Gl), 'r:', lw=3)
    ax.annotate('$V_0$='+str(np.round(El))+'mV, $\\tau_m$='+str(np.round(Tm))+\
                'ms, $g_L$='+str(np.round(Gl))+'nS', (0.1,.86), xycoords='axes fraction')
    set_plot(ax, ylabel='$V_m$ (mV)', xlabel='delay from state onset (ms)')
    return fig

def current_pulse_analysis(main):
    return fig_with_current_pulse_analysis(*get_stimulus_responses(main.filename))
    
if __name__ == '__main__':
    sys.path.append('../IO')
    from binary_to_python import load_file as BIN_load, get_metadata
    filename = sys.argv[-1]
    # make_fig(*get_stimulus_responses(filename))
    fig_with_current_pulse_analysis(*get_stimulus_responses(filename))
    plt.show()
else:
    from IO.binary_to_python import load_file as BIN_load, get_metadata
    

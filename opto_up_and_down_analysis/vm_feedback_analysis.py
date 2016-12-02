import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../')
from graphs.my_graph import set_plot

def get_stimulus_responses(filename, window=[-100e-3, 800e-3]):
    params = get_metadata(filename)
    t, [Vm, Iinj, LASER, UP_FLAG, Vm_LP, CMD] = BIN_load(filename)
    dt = (t[1]-t[0]) # dt in ms (transition times are stored in ms)
    t_window = window[0]+np.arange(int((window[1]-window[0])/dt)+1)*dt
    up_transitions = np.argwhere(np.diff(UP_FLAG)==1).flatten()
    down_transitions = np.argwhere(np.diff(UP_FLAG)==-1).flatten()

    TEST_TRACES, CTRL_TRACES = [], []
    TEST_COND = {'delay':[], 'amplitude':[], 'duration':[], 'times':[]}
    CTRL_COND = {'times':[]}
    
    if params['flag_for_state_stimulation']=='1': # if stimulation in Up state !
        for itup1, itup2 in zip(up_transitions[:-1], up_transitions[1:]):
            cond = (t>=t[itup1]+window[0]) & (t<=t[itup1]+window[1]) # conditions for analysis
            vv = Vm[cond]
            if len(vv)==len(t_window): # only if we are not in the borders to have same number of points
                # then we check whether there was a stimulation
                if np.diff(LASER[itup1:itup2]).max()>0:
                    # there was a laser input
                    i0 = np.argmax(np.diff(LASER[itup1:itup2]))
                    i1 = np.argmin(np.diff(LASER[itup1:])) # no limit, in case switch again...
                    TEST_TRACES.append(vv)
                    TEST_COND['times'].append(1e3*t[itup1])
                    TEST_COND['delay'].append(np.round(t[i0],2)*1e3)
                    TEST_COND['duration'].append(np.round(1e3*t[i1-i0],4))
                    TEST_COND['amplitude'].append(np.diff(LASER[itup1:itup2]).max())
                else: # no laser -> blank
                    CTRL_COND['times'].append(1e3*t[itup1])
                    CTRL_TRACES.append(vv)
                        
    elif params['flag_for_state_stimulation']=='2': # if stimulation in Down state !
        for itdown1, itdown2 in zip(down_transitions[:-1], down_transitions[1:]):
            cond = (t>=t[itdown1]+window[0]) & (t<=t[itdown1]+window[1]) # conditions for analysis
            vv = Vm[cond]
            if len(vv)==len(t_window): # only if we are not in the borders to have same number of points
                # then we check whether there was a stimulation
                if np.diff(LASER[itdown1:itdown2]).max()>0:
                    # there was a laser input
                    i0 = np.argmax(np.diff(LASER[itdown1:itdown2]))
                    i1 = np.argmin(np.diff(LASER[itdown1:])) # no limit, in case switch again...
                    TEST_TRACES.append(vv)
                    TEST_COND['times'].append(1e3*t[itdown1])
                    TEST_COND['delay'].append(np.round(t[i0],2)*1e3)
                    TEST_COND['duration'].append(np.round(1e3*t[i1-i0],4))
                    TEST_COND['amplitude'].append(np.diff(LASER[itdown1:itdown2]).max())
                else: # no laser -> blank
                    CTRL_COND['times'].append(1e3*t[itdown1])
                    CTRL_TRACES.append(vv)
    return 1e3*t_window, TEST_TRACES, CTRL_TRACES, TEST_COND, CTRL_COND, params


def fig_with_sample_traces(t_window, TEST_TRACES, CTRL_TRACES, delay, duration,\
                           threshold=-30, color='r', N=10):
    # then fig with all traces
    fig, ax = plt.subplots(1, figsize=(5,3.5))
    ax.set_title('delay='+str(delay)+'ms, duration='+str(duration)+'ms, n='+\
                 str(len(TEST_TRACES))+' trials',fontsize=12)
    plt.subplots_adjust(left=.2, bottom=.25)
    for v in CTRL_TRACES[:N]:
        ax.plot(t_window, v, 'k', lw=.5)
    ax.plot(t_window, CTRL_TRACES[-1], 'k',\
            label='blank trials \n (10 samples)', lw=.5)
    for v in TEST_TRACES[:N]:
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
                           threshold=-30, color='r'):
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
             threshold=-30, color='r'):
    FIGS = []
    delays, durations = np.unique(TEST_COND['delay']), np.unique(TEST_COND['duration'])
    for delay in delays:
        for duration in durations:
            i0 = np.argwhere((TEST_COND['delay']==delay) & (TEST_COND['duration']==duration)).flatten()
            #  ctrl trials (random pick !!) as the same number than test_trials
            i1 = np.random.choice(np.arange(len(CTRL_TRACES)), len(i0), replace=False)
            if len(i0)*len(i1)>1:
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
    fig, ax = plt.subplots(1, figsize=(6.5,4.5))
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
    El, Tm, Gl, func = fit_membrane_prop(t_window[tcond],\
                                         CTRL_TRACES.mean(axis=0)[tcond], params)
    ax.plot(t_window[tcond], func(t_window[tcond], El, Tm, Gl), 'r:', lw=3)
    ax.annotate('$V_0$='+str(np.round(El))+'mV, $\\tau_m$='+str(np.round(Tm))+\
                'ms, $g_L$='+str(np.round(Gl))+'nS', (0.1,.86), xycoords='axes fraction')
    set_plot(ax, ylabel='$V_m$ (mV)', xlabel='delay from state onset (ms)')
    return [fig]

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
    

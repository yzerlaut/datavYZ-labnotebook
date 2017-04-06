import numpy as np
import matplotlib.pyplot as plt
from IO.load_data import load_file, get_metadata
from graphs.interactive_view import FocusMenu
from graphs.my_graph import set_plot
import opto_up_and_down_analysis.choose_analysis as choose_ud_analysis
import classic_electrophy.choose_analysis as choose_ce_analysis
import modeling_work.choose_analysis as choose_mw_analysis

def plot_data(main):
    plt.close('all')
    main.params = get_metadata(main.filename)
    ## CHOOSING THE ANALYSIS
    func = choose_analysis(main) # function to analyze
    if func is None:
        FIG_LIST = [default_plot(main)]
    else: # a given analysis was actually implemented
        FIG_LIST = func(main)
    return FIG_LIST

def default_plot(main, xlabel='time (s)', ylabel=''):
    try:
        ylabel=np.array(['$V_m$ (mV)', '$I_m$ (pA)'])[int(main.params['clamp_index'])]
    except (KeyError, IndexError) :
        ylabel = ''
    t, VEC = load_file(main.filename, zoom=[main.args['x1'], main.args['x2']])
    fig = plt.figure(figsize=(10,6))
    # plt.subplots_adjust(left=.1, bottom=.15, hspace=0)
    plt.subplots_adjust(left=.2, bottom=.2, hspace=0)
    if len(VEC)>6: # means LFP
        ax = plt.subplot2grid((3,1), (0,0), rowspan=2)
        ax2 = plt.subplot2grid((3,1), (2,0))
        ax2.plot(t, 10*VEC[6], 'k-')
        set_plot(ax2, xlabel='time (s)', ylabel='LFP (uV)',\
             xlim=[main.args['x1'], main.args['x2']])
    else:
        ax = plt.subplot(111)
    ax.plot(t, VEC[0], 'k-')
    set_plot(ax, xlabel=xlabel, ylabel=ylabel,\
             xlim=[main.args['x1'], main.args['x2']],\
             ylim=[main.args['y1_min'], main.args['y1_max']])
    return fig

def save_as_npz(main, npz_file):
    t, VEC = load_file(main.filename, zoom=[main.args['x1'], main.args['x2']])
    to_be_executed = 'np.savez(npz_file, t=t'
    for i in range(len(VEC)):
        to_be_executed += ', v'+str(i+1)+'= VEC['+str(i)+']'
    to_be_executed += ')'
    exec(to_be_executed)

def choose_analysis(main):
    func = None
    if main.params['main_protocol']=='RT-opto-Up-Down':
        func = choose_ud_analysis.func_for_analysis(main)
    elif main.params['main_protocol']=='classic_electrophy':
        func = choose_ce_analysis.func_for_analysis(main)
    elif main.params['main_protocol']=='modeling_work':
        choose_mw_analysis.func_for_analysis(main)
    return func

def initialize_quantities_given_datafile(main, filename=None):
    # 
    if filename is None:
        filename = main.filename
    # 
    try:
        main.params = get_metadata(filename)
    except (FileNotFoundError, UnicodeDecodeError):
        pass
    
    if main.window2 is not None:
        # we clean up the actions of the previously used window
        main.window2.remove_actions()
        
    # if experimental data, channel 1 can have stored boundaries
    # whereas the other channels have automatic boundaries
    if main.params['main_protocol']!='modeling_work':
        args = {'x1':0., 'x2':3., 'dx':3.} # by default
        try:
            if main.params['cont_choice']=='False': # in case episode mode !
                args = {'x1':0., 'x2':float(main.params['episode_duration']), 'dx':float(main.params['episode_duration'])}
        except KeyError:
            pass
        t, VEC = load_file(filename, zoom=[args['x1'], args['x2']])
        for i in range(len(VEC)):
            exec("args['dy"+str(i+1)+"']=VEC["+str(i)+"].flatten().max()-VEC["+str(i)+"].flatten().min()")
            exec("if args['dy"+str(i+1)+"']==0: args['dy"+str(i+1)+"']=1")
            exec("args['y"+str(i+1)+"_min']=VEC["+str(i)+"].flatten().min()-args['dy"+str(i+1)+"']/10.")
            exec("args['y"+str(i+1)+"_max']=VEC["+str(i)+"].flatten().max()+args['dy"+str(i+1)+"']/10.")
        main.window2 = FocusMenu(main)
    else:
        args, main.window2 = {}, None
    return args


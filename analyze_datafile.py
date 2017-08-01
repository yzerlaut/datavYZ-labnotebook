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
    ## CHOOSING THE ANALYSIS
    func = choose_analysis(main) # function to analyze
    if func is None:
        FIG_LIST = [default_plot(main)]
    else: # a given analysis was actually implemented
        FIG_LIST = func(main)
    return FIG_LIST

def default_plot(main, xlabel='time (s)', ylabel=''):
    
    Nchannels = min([main.params['Nchannels'], 4]) # max 4 channels displayed
    
    fig, AX = plt.subplots(Nchannels, figsize=(30.,6.*Nchannels))
    plt.subplots_adjust(left=.15, bottom=.2, hspace=0.2, right=.95, top=.99)

    key_list = list(main.data.keys())
    key_list.remove("t")
    try:
        key_list.remove("params")
    except ValueError:
        pass
    
    cond = (main.data['t']>main.args['x1']) & (main.data['t']<=main.args['x2'])
    for i, key in enumerate(sorted(key_list)[:Nchannels]):
        AX[i].plot(main.data['t'][cond], main.data[key][cond])
        if i==Nchannels-1:
            set_plot(AX[i], xlabel=xlabel, ylabel=key, num_yticks=3)
        else:
            set_plot(AX[i], ['left'], ylabel=key, num_yticks=3, xticks=[])

    return fig

def save_as_npz(main, npz_file):
    data = load_file(main.filename, zoom=[main.args['x1'], main.args['x2']])
    data2 = {'params':data['params']}
    cond = (data['t']>=main.args['x1']) & (data['t']<=main.args['x2'])
    for key in data.keys():
        if key!='params':
            data2[key] = data[key][cond]
    np.savez(npz_file, **data2)
    print('sample of data saved as:', npz_file)

def choose_analysis(main):
    func = None
    if main.params['main_protocol']=='RT-opto-Up-Down':
        # func = choose_ud_analysis.func_for_analysis(main)
        func = None
    elif main.params['main_protocol']=='classic_electrophy':
        func = choose_ce_analysis.func_for_analysis(main)
    elif main.params['main_protocol']=='modeling_work':
        choose_mw_analysis.func_for_analysis(main)
    return func

def load_data_and_initialize(main):

    main.data = load_file(main.filename)
    main.params = get_metadata(main.filename)

    # print(main.data.keys())
    if main.window2 is not None:
        # we clean up the actions of the previously used window
        main.window2.remove_actions()

    main.args = {'x1':0.+main.params['tstart'], 'x2':3.+main.params['tstart'], 'dx':3.} # by default
    main.window2 = FocusMenu(main)


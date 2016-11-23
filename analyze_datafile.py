import numpy as np
import matplotlib.pyplot as plt
from IO.axon_to_python import load_file as ABF_load
from IO.binary_to_python import load_file as BIN_load, get_metadata
from graphs.interactive_view import FocusMenu
from graphs.my_graph import set_plot
import opto_up_and_down_analysis.choose_analysis as choose_ud_analysis

def plot_data(main):
    ## CHOOSING THE ANALYSIS
    plt.close('all')
    if len(main.filename.split('.abf'))>1:
        func = None
    elif (len(main.filename.split('.bin'))>1):
        main.params = get_metadata(main.filename)
        func = choose_analysis(main) # function to analyze
    else:
        func=None
    ## FINAL CHOICE
    if len(main.filename.split('.npz'))>1:
        # analysis within the datafile ! just execute it!
        data = np.load(main.filename)
        exec(str(data['plot']))
        FIG_LIST = []
        for i in plt.get_fignums():
            FIG_LIST.append(plt.figure(i))
    elif func is None:
        FIG_LIST = [default_plot(main)]
    else: # A GIVEN ANALYSIS WAS IMLEMENTED
        FIG_LIST = func(main)
    return FIG_LIST

def default_plot(main, xlabel='time (s)', ylabel='$V_m$ (mV)'):
    if len(main.filename.split('.abf'))>1:
        t, VEC = ABF_load(main.filename, zoom=[main.args['x1'], main.args['x2']])
    elif len(main.filename.split('.bin'))>1:
        t, VEC = BIN_load(main.filename, zoom=[main.args['x1'], main.args['x2']])
    fig, ax = plt.subplots(1, figsize=(10,5))
    plt.subplots_adjust(left=.1, bottom=.15)
    ax.plot(t, VEC[0], 'k-')
    set_plot(ax, xlabel=xlabel, ylabel=ylabel,\
             xlim=[main.args['x1'], main.args['x2']],\
             ylim=[main.args['y1_min'], main.args['y1_max']])
    return fig
    
def choose_analysis(main):
    func = None
    if main.params['main_protocol']=='RT-opto-Up-Down':
        func = choose_ud_analysis.func_for_analysis(main)
    return func

def initialize_quantities_given_datafile(main, filename=None):
    if main.window2 is not None:
        main.window2.remove_actions()
    if filename is None:
        filename = main.filename
    if (len(filename.split('.bin'))>1) or (len(filename.split('.abf'))>1):
        args = {'x1':0., 'x2':3., 'dx':3.}
        if len(filename.split('.bin'))>1:
            t, VEC = BIN_load(filename, zoom=[args['x1'], args['x2']])
        elif len(filename.split('.abf'))>1:
            t, VEC = ABF_load(filename, zoom=[args['x1'], args['x2']])
        for i in range(len(VEC)):
            exec("args['dy"+str(i+1)+"']=VEC["+str(i)+"].max()-VEC["+str(i)+"].min()")
            exec("if args['dy"+str(i+1)+"']==0: args['dy"+str(i+1)+"']=1")
            exec("args['y"+str(i+1)+"_min']=VEC["+str(i)+"].min()-args['dy"+str(i+1)+"']/10.")
            exec("args['y"+str(i+1)+"_max']=VEC["+str(i)+"].max()+args['dy"+str(i+1)+"']/10.")
        main.window2 = FocusMenu(main)
    elif (len(filename.split('.npz'))>1):
        args = {}
    else:
        args, main.window2 = None, None
    return args


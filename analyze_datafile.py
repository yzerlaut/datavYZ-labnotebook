import sys
import numpy as np
import matplotlib.pyplot as plt
from my_graph import set_plot
from IO.axon_to_python import load_file as ABF_load
from IO.elphy_to_python import get_analogsignals as DAT_load
from electrophy_data import FocusMenu

def plot_data(main):
    plt.close('all')
    if len(main.filename.split('.npz'))>1: # analysis within the datafile ! just execute it !
        data = np.load(main.filename)
        exec(str(data['plot']))
        FIG_LIST = []
        for i in plt.get_fignums():
            FIG_LIST.append(plt.figure(i))
    elif len(main.filename.split('.abf'))>1:
        t, v = ABF_load(main.filename, zoom=[main.args['x1'], main.args['x2']])
        fig, ax = plt.subplots(1, figsize=(10,5))
        plt.subplots_adjust(left=.1, bottom=.15)
        ax.plot(t, v, 'k-')
        set_plot(ax, xlabel='time (s)', ylabel='$V_m$ (mV)',\
                 xlim=[main.args['x1'], main.args['x2']],\
                 ylim=[main.args['y1'], main.args['y2']])
        FIG_LIST = [fig]
    elif len(main.filename.split('.DAT'))>1:
        data = DAT_load(main.filename, zoom=[main.args['x1'], main.args['x2']])
        t, v = data[0], data[1]
        fig, ax = plt.subplots(1, figsize=(10,5))
        plt.subplots_adjust(left=.1, bottom=.15)
        ax.plot(t, v, 'k-')
        set_plot(ax, xlabel='time (s)', ylabel='$V_m$ (mV)',\
                 xlim=[main.args['x1'], main.args['x2']],\
                 ylim=[main.args['y1'], main.args['y2']])
        FIG_LIST = [fig]
    return FIG_LIST


def initialize_quantities_given_datafile(main, filename=None):
    if filename is None:
        filename = main.filename
    if len(filename.split('.npz'))>1: # analysis within the datafile ! just execute it !
        window = None
    elif len(filename.split('.abf'))>1:
        main.args = {'x1':0., 'x2':3., 'dx':3., 'y1':-80., 'y2':0., 'dy':80.}
        window = FocusMenu(main)
    else:
        main.args, window = None, None
    return main.args, window


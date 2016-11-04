import sys
sys.path.append('../common_libraries/')
import numpy as np
import matplotlib.pyplot as plt
from graphs.my_graph import set_plot
from IO.fellin_lab import load_file

def generate_figs(DATA_FILE, args={'zoom':[0,3]}):
    plt.close('all')
    if len(DATA_FILE.split('.npz'))>1:
        data = np.load(DATA_FILE)
        exec(str(data['plot']))
        FIG_LIST = []
        for i in plt.get_fignums():
            FIG_LIST.append(plt.figure(i))
    if len(DATA_FILE.split('.abf'))>1:
        t, v = load_file(DATA_FILE, zoom=args['zoom'])
        fig, ax = plt.subplots(1, figsize=(10,5))
        plt.subplots_adjust(left=.1, bottom=.15)
        ax.plot(t, v, 'k-')
        set_plot(ax, xlabel='time (s)', ylabel='$V_m$ (mV)')
        FIG_LIST = [fig]
    return FIG_LIST


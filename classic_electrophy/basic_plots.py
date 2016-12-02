import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../')
from graphs.my_graph import set_plot, get_linear_colormap
from IO.binary_to_python import load_file as BIN_load, get_metadata

def plot_VC_episodes(main):
    t, VEC = BIN_load(main.filename, zoom=[main.args['x1'], main.args['x2']])
    y1, y2 = main.args['y1_min'], main.args['y1_max']
    fig = plt.figure(figsize=(10,7))
    plt.subplots_adjust(left=.15, bottom=.15, top=.96, right=.96)
    ax = plt.subplot2grid((3,1), (0,0), rowspan=2)
    mymap = get_linear_colormap(color1='blue', color2='red')
    for i in range(VEC.shape[1]):
        ax.plot(1e3*t, VEC[0][i], '-',\
                color=mymap(np.linspace(0,1,VEC.shape[1])[i],1))
    set_plot(ax, ['left'], ylabel='$I_{amp}$ (pA)',\
             xlim=[main.args['x1'], main.args['x2']], xticks=[],\
             ylim=[y1, y2])
    ax2 = plt.subplot2grid((3,1), (2,0))
    for i in range(VEC.shape[1]):
        ax2.plot(1e3*t, VEC[1][i], '-', alpha=.5,\
                color=mymap(np.linspace(0,1,VEC.shape[1])[i],1))
    set_plot(ax2, xlabel='time (ms)', ylabel='$V_A$ (mV)',\
             xlim=[main.args['x1'], main.args['x2']])
    return [fig]
    

def plot_IC_episodes(main):
    t, VEC = BIN_load(main.filename, zoom=[main.args['x1'], main.args['x2']])
    y1, y2 = main.args['y1_min'], main.args['y1_max']
    fig = plt.figure(figsize=(10,7))
    plt.subplots_adjust(left=.15, bottom=.15, top=.96, right=.96)
    ax = plt.subplot2grid((3,1), (0,0), rowspan=2)
    mymap = get_linear_colormap(color1='blue', color2='red')
    for i in range(VEC.shape[1]):
        ax.plot(1e3*t, VEC[0][i], '-',\
                color=mymap(np.linspace(0,1,VEC.shape[1])[i],1))
    set_plot(ax, ['left'], ylabel='$V_A$ (mV)',\
             xlim=[main.args['x1'], main.args['x2']], xticks=[],\
             ylim=[y1, y2])
    ax2 = plt.subplot2grid((3,1), (2,0))
    for i in range(VEC.shape[1]):
        ax2.plot(1e3*t, VEC[1][i], '-', alpha=.5,\
                color=mymap(np.linspace(0,1,VEC.shape[1])[i],1))
    set_plot(ax2, xlabel='time (ms)', ylabel='$I_{amp}$ (pA)',\
             xlim=[main.args['x1'], main.args['x2']])
    return [fig]
    


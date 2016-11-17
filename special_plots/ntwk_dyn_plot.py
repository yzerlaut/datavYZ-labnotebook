import sys
sys.path.append('../')
from graphs import my_graph
import matplotlib.pylab as plt
import numpy as np

def RASTER_PLOT(SPK_LIST, ID_LIST, tlim=None, ID_ZOOM_LIST=None, COLORS=None, with_fig=None, MS=1):
    
    if with_fig is not None:
        fig, ax = plt.gcf(), plt.gca()
    else:
        fig, ax = plt.subplots(1, figsize=(5, 3))
        plt.subplots_adjust(left=.25, bottom=.25)
        
    # time limit
    if tlim is None:
        tlim = np.ones(2)
        tlim[0] = np.min([np.min(spk) for spk in SPK_LIST])
        tlim[1] = np.max([np.max(spk) for spk in SPK_LIST])
    # neurons limit
    if ID_ZOOM_LIST is None:
        ID_ZOOM_LIST = []
        for ids in ID_LIST:
            ID_ZOOM_LIST.append([np.min(ids), np.max(ids)])
    # colors
    if COLORS is None:
        COLORS = ['g']+['r']+['k' for i in range(len(ID_LIST)-2)]

    ii=0 # index for plotting
    for spks, ids, id_zoom, col in zip(SPK_LIST, ID_LIST, ID_ZOOM_LIST, COLORS):
        spks2, ids2 = spks[(spks>=tlim[0]) & (spks<=tlim[1]) & (ids>=id_zoom[0]) & (ids<=id_zoom[1])], ids[(spks>=tlim[0]) & (spks<=tlim[1]) & (ids>=id_zoom[0]) & (ids<=id_zoom[1])]
        plt.plot(spks2, ii+ids2, '.', color=col, ms=MS)
        ii+=id_zoom[1]-id_zoom[0]
    tot_neurons_num = int(round(np.sum([(I[1]-I[0]) for I in ID_ZOOM_LIST])/100.,0)*100)
    ax.set_title(str(tot_neurons_num)+' neurons sample', fontsize=14)
    my_graph.set_plot(ax, xlabel='time (ms)', yticks=[], ylabel='neuron index')
    return fig, ax

def POP_ACT_PLOT(t, POP_ACT_LIST, tlim=None, pop_act_zoom=None, COLORS=None, with_fig=None):
    
    if with_fig is not None:
        fig, ax = plt.gcf(), plt.gca()
    else:
        fig, ax = plt.subplots(1, figsize=(5,3))
        plt.subplots_adjust(left=.25, bottom=.25)
    
    # time limit
    if tlim is None:
        tlim = [t.min(), t.max()]
    # pop act lim
    if pop_act_zoom is None:
        pop_act_zoom = np.zeros(2)
        pop_act_zoom[0] = np.min([np.min(act) for act in POP_ACT_LIST])
        pop_act_zoom[1] = np.max([np.max(act) for act in POP_ACT_LIST])
        ID_ZOOM_LIST = []
    # colors
    if COLORS is None:
        COLORS = ['g']+['r']+['k' for i in range(len(POP_ACT_LIST)-2)]

    for act, col in zip(POP_ACT_LIST[::-1], COLORS[::-1]):
        plt.plot(t[(t>=tlim[0]) & (t<=tlim[1])], act[(t>=tlim[0]) & (t<=tlim[1])], '-', color=col)
    my_graph.set_plot(ax, xlabel='time (ms)', ylabel='pop. act. (Hz)', ylim=pop_act_zoom)
    return fig, ax

if __name__=='__main__':

    RASTER_PLOT(
        [np.random.randn(3000),np.random.randn(1000)],
        [np.random.randint(3000, size=3000),np.random.randint(1000, size=1000)])
    
    plt.show()

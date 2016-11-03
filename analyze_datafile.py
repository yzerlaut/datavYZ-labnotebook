import numpy as np
import matplotlib.pyplot as plt
from graphs.my_graph import set_plot, put_list_of_figs_to_svg_fig

def generate_figs(DATA_FILE):
    if len(DATA_FILE.split('.npz'))>1:
        data = np.load(DATA_FILE)
        exec(str(data['plot']))
        FIG_LIST = []
        for i in plt.get_fignums():
            FIG_LIST.append(plt.figure(i))
    if len(DATA_FILE.split('.abf'))>1:
        print(DATA_FILE)
        FIG_LIST = []
    return FIG_LIST

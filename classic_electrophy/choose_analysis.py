from . import basic_plots
from . import vclamp_with_lfp
from . import cclamp_with_lfp
# from . import vm_feedback_analysis as vmfdbk
import sys
sys.path.append('../')
from IO.load_data import load_file, get_metadata

def func_for_analysis(main):
    if main.analysis_flag:
        print('not implemented yet !')
    else:
        if main.params['protocol']=='VCLAMP-WITH-THAL-AND-CORTEX-EXTRA':
            main.data = load_file(main.filename)
            return vclamp_with_lfp.plot_three_channels
        if main.params['protocol']=='ICLAMP-WITH-LFP':
            main.data = load_file(main.filename)
            return cclamp_with_lfp.plot_two_channels
        if main.params['protocol']=='VC-Membrane_Test':
            return basic_plots.plot_VC_episodes
        if main.params['protocol']=='F-I curve':
            return basic_plots.plot_IC_episodes
        elif main.params['protocol']=='Vm-feedback--Current-Pulses':
            return None
    

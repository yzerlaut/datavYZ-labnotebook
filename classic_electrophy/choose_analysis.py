from . import basic_plots
from . import vclamp_with_lfp
from . import cclamp_with_lfp
# from . import vm_feedback_analysis as vmfdbk

def func_for_analysis(main):
    if main.analysis_flag:
        print('not implemented yet !')
    else:
        print(main.params['protocol'])
        if main.params['protocol']=='VCLAMP-WITH-THAL-AND-CORTEX-EXTRA':
            print('ok to recoginze analysis')
            return vclamp_with_lfp.plot_three_channels
        if main.params['protocol']=='CCLAMP-WITH-CORTEX-EXTRA':
            print('ok to recoginze analysis')
            return cclamp_with_lfp.plot_two_channels
        if main.params['protocol']=='VC-Membrane_Test':
            return basic_plots.plot_VC_episodes
        if main.params['protocol']=='F-I curve':
            return basic_plots.plot_IC_episodes
        elif main.params['protocol']=='Vm-feedback--Current-Pulses':
            return None
    

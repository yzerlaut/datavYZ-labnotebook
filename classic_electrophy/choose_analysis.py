from . import basic_plots
# from . import vm_feedback_analysis as vmfdbk

def func_for_analysis(main):
    if main.analysis_flag:
        print('not implemented yet !')
    else:
        if main.params['protocol']=='VC-Membrane_Test':
            return basic_plots.plot_VC_episodes
        if main.params['protocol']=='F-I curve':
            return basic_plots.plot_IC_episodes
        elif main.params['protocol']=='Vm-feedback--Current-Pulses':
            return None
    

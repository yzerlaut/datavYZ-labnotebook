from neo.io import AxonIO
import numpy as np
import os
#import hdf5
from . import hdf5

def load_file(filename, zoom=[0,np.inf]):

    try:
        data = hdf5.load_dict_from_hdf5(filename)
        return data
    except FileNotFoundError:
        print('File not Found !')
        return {}

def get_protocol_name(filename):
    fn = filename.split(os.path.sep)[-1] # only the filename without path
    protocol = '' # empty by default
    if len(fn.split('_'))>0:
        fn2 = fn.split('_')
        for ss in fn2[3:-1]:
            protocol+=ss+'_'
        protocol += fn2[-1].split('.')[0] # removing extension
    return protocol

def get_metadata(filename):
    
    params = {'main_protocol':'undefined', 'protocol':'undefined'}
    # loading metadata
    data = load_file(filename, zoom=[0,np.inf])
    params['dt'] =  data['t'][1]-data['t'][0]
    params['tstart'] = data['t'][0]
    params['tstop'] = data['t'][-1]
    params['Nepisodes'] = 1 # Episode mode to be implemented
    params['Nchannels'] = len(data.keys())-2 # removing the time array and params
    
    # prtocol name in case
    protocol = get_protocol_name(filename)
    if protocol!='':
        params['protocol'] = protocol
        params['main_protocol'] = 'classic_electrophy'

    return params


if __name__ == '__main__':
    import hdf5
    import sys
    import matplotlib.pylab as plt
    filename = sys.argv[-1]
    print(get_metadata(filename))
    # data = load_file(filename, zoom=[-5.,np.inf])
    # # for i in range(10):
    # #     plt.plot(t, data[0][i])
    # plt.plot(data['t'], data['Ch1'])
    # plt.show()

from neo.io import AxonIO
import numpy as np
import os

def load_file(filename, zoom=[0,np.inf]):

    # loading the data file
    try:
        data = AxonIO(filename).read_block(lazy=False, cascade=True)
        dt =  float(data.segments[0].analogsignals[0].sampling_period)
        if zoom[0]<data.segments[0].analogsignals[0].t_start:
            zoom[0]=data.segments[0].analogsignals[0].t_start
        if zoom[1]>data.segments[-1].analogsignals[0].t_stop:
            zoom[1]=data.segments[-1].analogsignals[0].t_stop
        ### 
        ii = 0
        while (ii<len(data.segments)) and (float(data.segments[min(ii,len(data.segments)-1)].analogsignals[0].t_start)<=zoom[0]):
            ii+=1
        tt = np.array(data.segments[ii-1].analogsignals[0].times)
        cond = (tt>=zoom[0]) & (tt<=zoom[1])
        DATA = {'t':tt[cond]}

        for j in range(1, len(data.segments[ii-1].analogsignals)+1):
            DATA['Ch'+str(j)] = np.array(data.segments[ii-1].analogsignals[j-1])[cond]
        ### 
        while (ii<len(data.segments)) and ((float(data.segments[min(ii,len(data.segments)-1)].analogsignals[0].t_start)<=zoom[1])):
            tt = np.array(data.segments[ii].analogsignals[0].times)
            cond = (tt>=zoom[0]) & (tt<=zoom[1])
            DATA['t'] = np.concatenate([DATA['t'],\
                                        np.array(data.segments[ii].analogsignals[0].times)[cond]])
            for j in range(1, len(data.segments[ii].analogsignals)+1):
                DATA['Ch'+str(j)] = np.concatenate([DATA['Ch'+str(j)],\
                                                    np.array(data.segments[ii].analogsignals[j-1])[cond]])
            ii+=1
        return DATA
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
    data = AxonIO(filename).read_block(lazy=False, cascade=True)
    params['dt'] =  float(data.segments[0].analogsignals[0].sampling_period)
    params['tstart'] = float(data.segments[0].analogsignals[0].times[0])
    params['tstop'] = float(data.segments[0].analogsignals[0].times[-1])
    params['Nepisodes'] = len(data.segments)
    params['Nchannels'] = len(data.segments[0].analogsignals)
    
    # prtocol name in case
    protocol = get_protocol_name(filename)
    if protocol!='':
        params['protocol'] = protocol
        params['main_protocol'] = 'classic_electrophy'

    return params


if __name__ == '__main__':
    import sys
    import matplotlib.pylab as plt
    filename = sys.argv[-1]
    data = AxonIO(filename).read_block(lazy=False, cascade=True)
    print(get_metadata(filename))
    # data = load_file(filename, zoom=[-5.,np.inf])
    # # for i in range(10):
    # #     plt.plot(t, data[0][i])
    # plt.plot(data['t'], data['Ch1'])
    # plt.show()

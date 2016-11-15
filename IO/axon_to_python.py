from neo.io import AxonIO
import numpy as np

def load_file(filename, zoom=[0,np.inf]):

    # loading the data file
    try:
        data = AxonIO(filename).read_block()
        dt =  float(data.segments[0].analogsignals[0].sampling_period)
        if zoom[0]<data.segments[0].analogsignals[0].t_start:
            zoom[0]=data.segments[0].analogsignals[0].t_start
        if zoom[1]>data.segments[-1].analogsignals[0].t_stop:
            zoom[1]=data.segments[-1].analogsignals[0].t_stop
        ### 
        ii = 0
        while float(data.segments[ii].analogsignals[0].t_start)<=zoom[0]:
            ii+=1
        tt = np.array(data.segments[ii-1].analogsignals[0].times)
        cond = (tt>=zoom[0]) & (tt<=zoom[1])
        VEC = [tt[cond]]
        for j in range(1, len(data.segments[ii-1].analogsignals)+1):
            VEC.append(np.array(data.segments[ii-1].analogsignals[j-1])[cond])
        ### 
        while ((float(data.segments[ii].analogsignals[0].t_start)<=zoom[1]) and (ii<len(data.segments))):
            tt = np.array(data.segments[ii].analogsignals[0].times)
            cond = (tt>=zoom[0]) & (tt<=zoom[1])
            VEC[0] = np.concatenate([VEC[0],\
                np.array(data.segments[ii].analogsignals[0].times)[cond]])
            for j in range(1, len(data.segments[ii].analogsignals)+1):
                VEC[j] = np.concatenate([VEC[j],\
                    np.array(data.segments[ii].analogsignals[j-1])[cond]])
            ii+=1
        return VEC[0], VEC[1:]
    except FileNotFoundError:
        print('File not Found !')
        return [[], []]
    

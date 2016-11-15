import numpy as np
import json

def load_file(filename, zoom=[0,np.inf]):

    P = get_metadata(filename)
    nChannels = int(P['ChannelCount'])
    nEpisode = int(P['EpCount'])
    dt = 1e-3/float(P['f_acq'])
    # loading the data file
    try:
        data = np.fromfile(filename, dtype=np.float32)
        npoints = int(len(data)/int(P['ChannelCount']))
        t = np.arange(npoints)*dt
        if int(P['EpCount'])==1:
            data = data.reshape(nChannels,npoints)
        else:
            print('========================================')
            print('Need to implement the Episode Mode in loading File !!')
            print('========================================')
        return t[(t>=zoom[0]) & (t<=zoom[1])], [data[i][(t>=zoom[0]) & (t<=zoom[1])] for i in range(nChannels)]
    except FileNotFoundError:
        print('File not Found !')
        return [[], []]

def get_metadata(filename):
    with open(filename.replace('data.bin', 'metadata.json'), 'r') as json_data:
        data=json_data.read().replace('\n', '').replace('\\', '\\\\')
        params = json.loads(data)
        return params
    
if __name__ == '__main__':
    import sys
    import matplotlib.pylab as plt
    filename = sys.argv[-1]
    t, data = load_file(filename, zoom=[0,2.3])
    plt.plot(t, data[0])
    plt.show()

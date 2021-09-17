#!/home/meichen/anaconda3/bin/python

import numpy as np
import matplotlib.pyplot as plt
import obspy

fc1 = np.linspace(0.05,1.0,100) # Hz
fc2 = np.linspace(0.05,1.0,100) # Hz
delay = np.linspace(0,10,100) # delay time of the second asperity in seconds

peakamp1 = 0.3 # peak amplitude of the first asperity
peakamp2 = 0.7 # peak amplitude of the second asperity
source_duration = 20 # source duration is 20 seconds
delta = 0.1 # sampling rate is 0.1 second
N = np.int(source_duration/delta) # number of point in frequency domain

for i in np.arange(len(fc1)):
    for j in np.arange(len(fc2)):
        for k in np.arange(len(delay)):
            N_delay = np.int(delay[k]/delta)
            fcm = (1.0/delta)/2.0
            f = np.linspace(0.01,fcm,N)
            sp1 = 1/(1+f**2/fc1[i]**2)
            sp2 = 1/(1+f**2/fc2[j]**2)
            spec1 = np.hstack((sp1,sp1[-1:0:-1]*(-1.0)))
            spec2 = np.hstack((sp2,sp2[-1:0:-1]*(-1.0)))
            
            stf1 = np.fft.ifft(spec1)
            stf2 = np.fft.ifft(spec2)
            y1 = abs(stf1[0:N])
            y1 = y1/np.max(y1)
            y2 = abs(stf2[0:N])
            y2 = y2/np.max(y2)
            y = []
            for m in np.arange(len(y1)):
                if(m<N_delay):
                    y.append(y1[m]*peakamp1)
                else:
                    y.append(y1[m]*peakamp1+y2[m-N_delay]*peakamp2)
            
            y = np.array(y)
            y = y / np.sum(y)
            
            header = {'delta':delta}
            sac = obspy.io.sac.SACTrace(data=y,**header)
            sac.write('stf_{%4.2f}_{%4.2f}_{%4.2f}.sac'.format(fc1[i],fc2[j],delay[k]),byteorder='big')


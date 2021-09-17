#!/home/meichen/anaconda3/bin/python

import numpy as np
import matplotlib.pyplot as plt
import obspy

fc1 = 0.2 # Hz
fc2 = 0.6 # Hz
source_duration = 10 # source duration is 20 seconds
delta = 0.1 # sampling rate is 0.1 second
N = np.int(source_duration/delta) # number of point in frequency domain
delay = 2 # delay time of the second asperity in seconds
N_delay = np.int(delay/delta)
peakamp1 = 0.3 # peak amplitude of the first asperity
peakamp2 = 0.7 # peak amplitude of the second asperity

fcm = (1.0/delta)/2.0
f = np.linspace(0.01,fcm,N)
sp1 = 1/(1+f**2/fc1**2)
sp2 = 1/(1+f**2/fc2**2)
spec1 = np.hstack((sp1,sp1[-1:0:-1]*(-1.0)))
spec2 = np.hstack((sp2,sp2[-1:0:-1]*(-1.0)))

stf1 = np.fft.ifft(spec1)
stf2 = np.fft.ifft(spec2)
y1 = abs(stf1[0:N])
y1 = y1/np.max(y1)
y2 = abs(stf2[0:N])
y2 = y2/np.max(y2)
y = []
for i in np.arange(len(y1)):
    if(i<N_delay):
        y.append(y1[i]*peakamp1)
    else:
        y.append(y1[i]*peakamp1+y2[i-N_delay]*peakamp2)
        

y = np.array(y)
y = y / np.sum(y)

moment_sum = 0.
for i in np.arange(len(y)):
    moment_sum = moment_sum + y[i]
    if(moment_sum>0.9):
        print(i*delta)
        break
fig,ax = plt.subplots(2,1,figsize=[8,5])
ax[0].plot(y1,'r-',lw=0.5,label='fc={}'.format(fc1))
ax[0].plot(y2,'b-',lw=0.5,label='fc={}'.format(fc2))
ax[0].legend()
ax[1].plot(y,'k-',lw=1)
plt.show()
header = {'delta':delta}
sac = obspy.io.sac.SACTrace(data=y,**header)
sac.write('stf_master.sac',byteorder='big')


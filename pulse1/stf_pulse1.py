#!/home/meichen/anaconda3/bin/python

import numpy as np
import matplotlib.pyplot as plt
import obspy

fc = 1.0 # Hz
source_duration = 10 # source duration is 20 seconds
delta = 0.1 # sampling rate is 0.1 second
N = np.int(source_duration/delta) # number of point in frequency domain

fcm = (1.0/delta)/2.0
f = np.linspace(0.01,fcm,N)
sp = 1/(1+f**2/fc**2)
spec = np.hstack((sp,sp[-1:0:-1]*(-1.0)))

stf = np.fft.ifft(spec)
y = abs(stf[0:N])
y = np.array(y)
y = y / np.sum(y)

moment_sum = 0.
for i in np.arange(len(y)):
    moment_sum = moment_sum + y[i]
    if(moment_sum>0.9):
        print(i*delta)
        break
fig,ax = plt.subplots(1,1,figsize=[5,3])
ax.plot(y,'k-',lw=1)
plt.show()
header = {'delta':delta}
sac = obspy.io.sac.SACTrace(data=y,**header)
sac.write('stf_egf.sac',byteorder='big')


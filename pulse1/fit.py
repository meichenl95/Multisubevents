#!/home/meichen/anaconda3/bin/python

import numpy as np
import matplotlib.pyplot as plt
from sys import argv
import sys
from scipy.optimize import curve_fit


def func(x,a,b,c):
    return np.log10(a) + np.log10(1 + x**2/b**2) - np.log10(1 + x**2/c**2)


data = np.genfromtxt('{}'.format(argv[1]))
freq = data[:,0]
amp = data[:,1]

popt,pcov = curve_fit(func,freq,np.log10(amp),bounds=([1.0,0.0,0.0],[1000,10,10]),method='trf',loss='huber',f_scale=0.1)

fig,ax = plt.subplots(1,1,figsize=[8,4])
ax.plot(freq,amp,'k-',lw=1,label=r'$M_0^m/M_0^{eGf}=31.6, f_c^{eGf}=1, f_c^M=0.5 $')
ax.plot(freq,10**(func(freq,*popt)),color='gray',ls='--',lw=2,alpha=0.7,label=r'$M_0^m/M_0^{eGf}=%4.1f, f_c^{eGf}=%4.2f, f_c^M=%4.2f $' % (popt[0],popt[1],popt[2]))
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Frequency(Hz)',size=16)
ax.set_ylabel('Amp',size=16)
fig.legend(loc=10)
fig.tight_layout()
plt.savefig('fit.png')

from matplotlib import markers
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
plt.rcParams.update({'font.sans-serif'	: 'Helvatica',
					'font.family'		: 'sans-serif', 
					'font.size'			: 20,
					'font.weight'		: 'regular',
					'xtick.labelsize'	: 16,
					'ytick.labelsize'	: 16,
					'axes.linewidth'	: 2})

#sysnames22      = ['c0-mbn', 'c12-mbn', 'c6-mbn', 'c11-mbn']
sysnames22      = ['c12-mbn', 'c6-mbn', 'c11-mbn']
#sysnames100     = ['c0-mbn-100', 'c12-mbn-100', 'c6-mbn-100', 'c11-mbn-100']  
sysnames100     = ['c12-mbn-100', 'c6-mbn-100', 'c11-mbn-100']  
plotnames       = {'c6-mbn' : r"$C_{6}H_{12}FEC$"+'\n+4MBN', 'c11-mbn' : r"$C_{11}H_{22}FEC$"+'\n+4MBN', 'c12-mbn' : r"$C_{12}H_{25}$"+'\n+4MBN', 'c0-mbn' : r"$4MBN$", 'c6-mbn-100' : r"$C_{6}H_{12}FEC$"+'\n+4MBN', 'c11-mbn-100' : r"$C_{11}H_{22}FEC$"+'\n+4MBN', 'c12-mbn-100' : r"$C_{12}H_{25}$"+'\n+4MBN', 'c0-mbn-100' : r"$4MBN$"}

stark           = 3.6
shift_mean_mbn  = []
shift_mean_nombn= []
dummy           = [plotnames[sysname] for sysname in sysnames22]

for sysname in sysnames22:
    fname1   = sysname + '_field_inter_mbn.dat'
    fname2   = sysname + '_field_inter_nombn.dat'
    data1    = np.loadtxt(fname1, dtype=float)
    data2    = np.loadtxt(fname2, dtype=float)
    freq1    = -1.0 * stark * np.mean(data1)
    freq2    = -1.0 * stark * np.mean(data2)
    #print(np.mean(data1), ',', np.mean(data2))
    shift_mean_mbn.append(freq1)
    shift_mean_nombn.append(freq2)

fig, ax     = plt.subplots(figsize=(7, 6))
#plt.ylim(-30,-10)
plt.plot(dummy, shift_mean_mbn, marker="s", color='blue')#, linestyle='None')
plt.plot(dummy, shift_mean_nombn, marker="s", color='black')#, linestyle='None')
ax.set(xlabel='system', ylabel=r"$\Delta\nu_{CN} (cm^{-1})$")
fig.tight_layout()
plt.savefig('freq_22.png', transparent=True, quality=100)
plt.clf()

shift_mean_mbn  = []
shift_mean_nombn= []
dummy           = [plotnames[sysname] for sysname in sysnames100]

for sysname in sysnames100:
    fname1   = sysname + '_field_inter_mbn.dat'
    fname2   = sysname + '_field_inter_nombn.dat'
    data1    = np.loadtxt(fname1, dtype=float)
    data2    = np.loadtxt(fname2, dtype=float)
    freq1    = -1.0 * stark * np.mean(data1)
    freq2    = -1.0 * stark * np.mean(data2)
    print(np.mean(data1), ',', np.mean(data2))
    shift_mean_mbn.append(freq1)
    shift_mean_nombn.append(freq2)

fig, ax     = plt.subplots(figsize=(7, 6))
#plt.ylim(-30,0)
plt.plot(dummy, shift_mean_mbn, marker="s", color='blue')#, linestyle='None')
plt.plot(dummy, shift_mean_nombn, marker="s", color='black')#, linestyle='None')
ax.set(xlabel='system', ylabel=r"$\Delta\nu_{CN} (cm^{-1})$")
fig.tight_layout()
plt.savefig('freq_100.png', transparent=True, quality=100)
plt.clf()
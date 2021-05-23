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

sysnames22      = ['c0-mbn', 'c12-mbn', 'c6-mbn', 'c11-mbn']
sysnames100     = ['c0-mbn-100', 'c12-mbn-100', 'c6-mbn-100', 'c11-mbn-100']  
plotnames       = {'c6-mbn' : r"$C_{6}H_{12}FEC+4MBN$", 'c11-mbn' : r"$C_{11}H_{22}FEC+4MBN$", 'c12-mbn' : r"$C_{12}H_{25}+4MBN$", 'c0-mbn' : r"$4MBN$", 'c6-mbn-100' : r"$C_{6}H_{12}FEC+4MBN$", 'c11-mbn-100' : r"$C_{11}H_{22}FEC+4MBN$", 'c12-mbn-100' : r"$C_{12}H_{25}+4MBN$", 'c0-mbn-100' : r"$4MBN$"}

stark           = 3.6
lig = []
mbn = []
sol = []
dummy           = [0, 1, 2, 3]

for sysname in sysnames22:
    fname1   = sysname + '_field_lig.dat'
    fname2   = sysname + '_field_mbn.dat'
    fname3   = sysname + '_field_sol.dat'
    data1    = np.loadtxt(fname1, dtype=float)
    data2    = np.loadtxt(fname2, dtype=float)
    data3    = np.loadtxt(fname3, dtype=float)
    lig.append(np.mean(data1))
    mbn.append(np.mean(data2))
    sol.append(np.mean(data3))

fig, ax     = plt.subplots(figsize=(7, 6))
#plt.ylim(-30,-10)
plt.plot(dummy, lig, marker="s", color='black', linestyle='None')
plt.plot(dummy, mbn, marker="s", color='blue', linestyle='None')
plt.plot(dummy, sol, marker="s", color='red', linestyle='None')
ax.set(xlabel='system', ylabel=r"$field$")
fig.tight_layout()
plt.savefig('decompose_22.png', transparent=True, quality=100)
plt.clf()

lig = []
mbn = []
sol = []
dummy           = [0, 1, 2, 3]

for sysname in sysnames100:
    fname1   = sysname + '_field_lig.dat'
    fname2   = sysname + '_field_mbn.dat'
    fname3   = sysname + '_field_sol.dat'
    data1    = np.loadtxt(fname1, dtype=float)
    data2    = np.loadtxt(fname2, dtype=float)
    data3    = np.loadtxt(fname3, dtype=float)
    lig.append(np.mean(data1))
    mbn.append(np.mean(data2))
    sol.append(np.mean(data3))

fig, ax     = plt.subplots(figsize=(7, 6))
#plt.ylim(-30,-10)
plt.plot(dummy, lig, marker="s", color='black', linestyle='None')
plt.plot(dummy, mbn, marker="s", color='blue', linestyle='None')
plt.plot(dummy, sol, marker="s", color='red', linestyle='None')
ax.set(xlabel='system', ylabel=r"$field$")
fig.tight_layout()
plt.savefig('decompose_100.png', transparent=True, quality=100)
plt.clf()

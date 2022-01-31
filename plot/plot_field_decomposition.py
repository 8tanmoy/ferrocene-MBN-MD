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
#sysnames100     = ['c0-mbn-100', 'c12-mbn-100', 'c6-mbn-100', 'c11-mbn-100']  
#sysnames22      = ['c12-mbn', 'c6-mbn', 'c11-mbn']
sysnames100     = ['c12-mbn-100', 'c6-mbn-100', 'c11-mbn-100']  
plotnames       = {'c6-mbn' : r"$C_{6}H_{12}FEC$"+'\n+4MBN', 'c11-mbn' : r"$C_{11}H_{22}FEC$"+'\n+4MBN', 'c12-mbn' : r"$C_{12}H_{25}$"+'\n+4MBN', 'c0-mbn' : r"$4MBN$", 'c6-mbn-100' : r"$C_{6}H_{12}FEC$"+'\n+4MBN', 'c11-mbn-100' : r"$C_{11}H_{22}FEC$"+'\n+4MBN', 'c12-mbn-100' : r"$C_{12}H_{25}$"+'\n+4MBN', 'c0-mbn-100' : r"$4MBN$"}

stark           = 3.6
lig = []
mbn = []
sol = []
inter_mbn = []
inter_nombn = []
dummy       = [plotnames[sysname] for sysname in sysnames22]

for sysname in sysnames22:
    fname1   = sysname + '_nu_lig.dat'
    fname2   = sysname + '_nu_mbn.dat'
    fname3   = sysname + '_nu_sol.dat'
    fname4   = sysname + '_nu_inter_mbn.dat'
    fname5   = sysname + '_nu_inter_nombn.dat'
    data1    = np.loadtxt(fname1, dtype=float)
    data2    = np.loadtxt(fname2, dtype=float)
    data3    = np.loadtxt(fname3, dtype=float)
    data4    = np.loadtxt(fname4, dtype=float)
    data5    = np.loadtxt(fname5, dtype=float)
    lig.append(np.mean(data1))
    mbn.append(np.mean(data2))
    sol.append(np.mean(data3))
    inter_mbn.append(np.mean(data4))
    inter_nombn.append(np.mean(data5))

fig, ax     = plt.subplots(figsize=(8.5, 6))
plt.ylim(-3,10)
plt.plot(dummy, lig, marker="s", color='black', label='Ligand'  )#, linestyle='None')
plt.plot(dummy, mbn, marker="s", color='blue',  label=r"$4MBN$" )#, linestyle='None')
plt.plot(dummy, sol, marker="s", color='red',   label="$Water$" )#, linestyle='None')
plt.plot(dummy, inter_mbn, marker="o", color='grey', label="$Inter \: with \: 4MBN$", linestyle='dotted')
plt.plot(dummy, inter_nombn, marker="o", color='grey', label="$Inter \: no \: 4MBN$", linestyle='dashed')
ax.set(xlabel='system', ylabel=r"$\Delta \nu (cm^{-1})$")
ax.legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, fontsize=14)
plt.subplots_adjust(right=0.9)
fig.tight_layout()
plt.savefig('decompose_22.png', transparent=True, quality=100)
plt.clf()
'''
lig = []
mbn = []
sol = []
inter_mbn = []
inter_nombn = []
dummy           = [plotnames[sysname] for sysname in sysnames100]

for sysname in sysnames100:
    fname1   = sysname + '_field_lig.dat'
    fname2   = sysname + '_field_mbn.dat'
    fname3   = sysname + '_field_sol.dat'
    fname4   = sysname + '_field_inter_mbn.dat'
    fname5   = sysname + '_field_inter_nombn.dat'
    data1    = np.loadtxt(fname1, dtype=float)
    data2    = np.loadtxt(fname2, dtype=float)
    data3    = np.loadtxt(fname3, dtype=float)
    data4    = np.loadtxt(fname4, dtype=float)
    data5    = np.loadtxt(fname5, dtype=float)
    lig.append(np.mean(data1))
    mbn.append(np.mean(data2))
    sol.append(np.mean(data3))
    inter_mbn.append(np.mean(data4))
    inter_nombn.append(np.mean(data5))

fig, ax     = plt.subplots(figsize=(8.5, 6))
plt.ylim(-4.5,8)
plt.plot(dummy, lig, marker="s", color='black',  label='Ligand'  )#, linestyle='None')
plt.plot(dummy, mbn, marker="s", color='blue',   label=r"$4MBN$" )#, linestyle='None')
plt.plot(dummy, sol, marker="s", color='red',    label="$Water$" )#, linestyle='None')
plt.plot(dummy, inter_mbn, marker="o", color='grey', label="$Inter \: with \: 4MBN$", linestyle='dotted')
plt.plot(dummy, inter_nombn, marker="o", color='grey', label="$Inter \: no \: 4MBN$", linestyle='dashed')
ax.set(xlabel='system', ylabel=r"$Field (V\: nm^{-1})$")
ax.legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, fontsize=14)
plt.subplots_adjust(right=0.9)
fig.tight_layout()
plt.savefig('decompose_100.png', transparent=True, quality=100)
plt.clf()
'''

#!/opt/anaconda3/bin/python3
#-- plot number densities for ferrocene-MBN simulations --

from os import system
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
plt.rcParams.update({'font.sans-serif'	: 'Helvatica',
					'font.family'		: "sans-serif", 
					'font.size'			: 20,
					'font.weight'		: 'regular',
					'xtick.labelsize'	: 16,
					'ytick.labelsize'	: 16,
					'axes.linewidth'	: 1.5})

#--load files--
sysnames	= ['c6-mbn', 'c11-mbn', 'c12-mbn', 'c0-mbn']
plotnames	= {'c6-mbn' : r"$C_{6}H_{12}FEC+4MBN$", 'c11-mbn' : r"$C_{11}H_{22}FEC+4MBN$", 'c12-mbn' : r"$C_{12}H_{25}+4MBN$", 'c0-mbn' : r"$4MBN$"}
dfs_n		= {}
dfs_dip = {}
for sysname in sysnames:
    fname_n			= sysname + '_rho_n.xvg'
    fname_dip       = sysname + '_order.xvg'
    dfs_n[sysname]	= pd.read_csv(fname_n ,skiprows=29, header=None, delim_whitespace=True)
    peakpos_aus		= np.argmax(dfs_n[sysname][1])
    peak_aus		= abs(dfs_n[sysname][0][peakpos_aus])
    print(sysname, peak_aus)
    dfs_dip[sysname]= pd.read_csv(fname_dip, skiprows=17, header=None, delim_whitespace=True)
    poslist         = dfs_dip[sysname][0].tolist()
    midpos          = (poslist[-1] - poslist[0])*0.5
    print('midpos: ', midpos)
    dfs_dip[sysname][0] -= midpos
    dfs_dip[sysname][0] -= peak_aus

custom_xlim = (0.0, 1.50)
custom_ylim = (-0.6, 0.6)

fig, axs = plt.subplots(1, 1, sharex=True, sharey=True)
fig.set_figwidth(8)
fig.set_figheight(6)
plt.setp(axs, xlim=custom_xlim, ylim=custom_ylim)

for sysname in sysnames:
    df = dfs_dip[sysname]
    axs.plot(df[0], df[4], lw=2.5, label=f"{plotnames[sysname]}")

plt.legend(fontsize=14, loc='upper right')
plt.tight_layout()
fig.subplots_adjust(bottom=0.12, left=0.18)
fig.text(0.5, 0.02, r"$Z(nm)$", ha='center')
fig.text(0.02, 0.55, r"$Cosine \: of \: water \: dipoles \: with \: normal$",va='center' ,rotation='vertical')
plt.savefig('dipole_22.png', transparent=True, quality=100)
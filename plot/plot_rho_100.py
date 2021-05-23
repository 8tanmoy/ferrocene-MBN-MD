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
sysnames	= ['c6-mbn-100', 'c11-mbn-100', 'c12-mbn-100', 'c0-mbn-100']
plotnames	= {'c6-mbn-100' : r"$C_{6}H_{12}FEC+4MBN$", 'c11-mbn-100' : r"$C_{11}H_{22}FEC+4MBN$", 'c12-mbn-100' : r"$C_{12}H_{25}+4MBN$", 'c0-mbn-100' : r"$4MBN$"}

dfs_n		= {}
dfs_c       = {}
z_aus		= {}

for sysname in sysnames:
    fname_n			= sysname + '_rho_n.xvg'
    fname_c         = sysname + '_rho_c.xvg'
    dfs_n[sysname]	= pd.read_csv(fname_n ,skiprows=27, header=None, delim_whitespace=True)
    dfs_c[sysname]	= pd.read_csv(fname_c ,skiprows=27, header=None, delim_whitespace=True)
    peakpos_aus		= np.argmax(dfs_n[sysname][1])
    peak_aus		= abs(dfs_n[sysname][0][peakpos_aus])
    print(sysname, peak_aus)
    z_aus[sysname]	= dfs_n[sysname][0] - peak_aus
#------------------ plot rho_n ------------------
custom_xlim = (0.0, 3.0)
custom_ylim = (0, 20)

fig, axs = plt.subplots(3, 1, sharex=True, sharey=True)
fig.set_figwidth(6)
fig.set_figheight(11)
plt.setp(axs, xlim=custom_xlim, ylim=custom_ylim)

AUS_COL = 'limegreen'

for ii in range(3):
	sysname = sysnames[ii]
	df = dfs_n[sysname]
	axs[ii].fill_between(z_aus[sysname], df[1].tolist(), color=AUS_COL, label='AUS',     alpha=0.5)
	axs[ii].plot(z_aus[sysname], (df[4]*0.5).tolist(),   color='cyan' , label='OW/2',   lw=2, alpha=0.5)
	axs[ii].plot(z_aus[sysname], df[2].tolist(),         color='blue',   label='NZ',     lw=2)
	if 'c12' in sysname:
		axs[ii].plot(z_aus[sysname], df[3].tolist(),         color='red',    label='C12',     lw=2)
	else:
		axs[ii].plot(z_aus[sysname], df[3].tolist(),         color='red',    label='FE',     lw=2)
	axs[ii].set_title(f"{plotnames[sysname]}", fontsize=16 )
	axs[ii].legend(fontsize=14, loc='lower right')

for ax in axs.flat:
    ax.label_outer()
plt.tight_layout()
fig.subplots_adjust(bottom=0.08, left=0.15)
fig.text(0.5, 0.02, r"$Z(nm)$", ha='center')
fig.text(0.01, 0.5, r"$Number \, density\, (nm^{-3})$",va='center' ,rotation='vertical')
plt.savefig('rho_n_100.png', transparent=True, quality=100)

#------------------ plot rho_c ------------------
#custom_xlim = (0.0, 1.50)
custom_ylim = (-10, 10)

fig, axs = plt.subplots(3, 1, sharex=True, sharey=True)
fig.set_figwidth(6)
fig.set_figheight(11)
plt.setp(axs, xlim=custom_xlim)#, ylim=custom_ylim)

AUS_COL = 'limegreen'

for ii in range(3):
	sysname = sysnames[ii]
	df = dfs_c[sysname]
	axs[ii].hlines(0, custom_xlim[0], custom_xlim[1], lw=1, color='black')
	axs[ii].plot(z_aus[sysname], df[1].tolist(),   color='purple' , label='System', lw=2)
	axs[ii].plot(z_aus[sysname], df[2].tolist(),   color='blue',   label='MBN',     lw=2)
	axs[ii].plot(z_aus[sysname], df[3].tolist(),   color='red',    label='R-FEC',   lw=2)
	axs[ii].plot(z_aus[sysname], df[4].tolist(),   color='cyan',    label='SOL',   lw=2)
	axs[ii].set_title(f"{plotnames[sysname]}", fontsize=16 )
	axs[ii].legend(fontsize=14, loc='lower right')

for ax in axs.flat:
    ax.label_outer()
plt.tight_layout()
fig.subplots_adjust(bottom=0.08, left=0.15)
fig.text(0.5, 0.02, r"$Z(nm)$", ha='center')
fig.text(0.01, 0.5, r"$Charge \, density\, (e.nm^{-3})$",va='center' ,rotation='vertical')
plt.savefig('rho_c_100.png', transparent=True, quality=100)

plt.clf()

#------------ separate c0 plot -----------
custom_xlim = (0.0, 3.0)
custom_ylim = (0, 20)
fig, axs = plt.subplots(1, 1, sharex=True, sharey=True)
fig.set_figwidth(6)
fig.set_figheight(4.00)
plt.setp(axs, xlim=custom_xlim, ylim=custom_ylim)
ii = 3
sysname = sysnames[ii]
df		= dfs_n[sysname]
axs.fill_between(z_aus[sysname], df[1].tolist(), color=AUS_COL, label='AUS',     alpha=0.5)
axs.plot(z_aus[sysname], df[2].tolist(),         color='blue',   label='NZ',     lw=2)
axs.set_title(f"{plotnames[sysname]}", fontsize=16 )
axs.legend(fontsize=14, loc='upper right')
plt.tight_layout()
fig.subplots_adjust(bottom=0.19, left=0.15)
fig.text(0.5, 0.02, r"$Z(nm)$", ha='center')
fig.text(0.01, 0.5, r"$Number \, density\, (nm^{-3})$",va='center' ,rotation='vertical')
plt.savefig('rho_n_100_c0-mbn.png', transparent=True, quality=100)
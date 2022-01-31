from locale import D_FMT
from turtle import width
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import sys
plt.rcParams.update({'font.sans-serif'	: 'Helvatica',
					'font.family'		: "sans-serif", 
					'font.size'			: 20,
					'font.weight'		: 'regular',
					'xtick.labelsize'	: 16,
					'ytick.labelsize'	: 16,
					'axes.linewidth'	: 1.5})

sysnames	= ['c0-mbn', 'c12-mbn', 'c6-mbn', 'c11-mbn']
titlenames	= {'c6-mbn' : r"$C_{6}H_{12}FEC+4MBN$", 'c11-mbn' : r"$C_{11}H_{22}FEC+4MBN$", 'c12-mbn' : r"$C_{12}H_{25}+4MBN$", 'c0-mbn' : r"$4MBN$"}

fig, axs	= plt.subplots(4, 1, figsize=(24, 16), sharex=True, sharey=True)
custom_ylim = (-40, 40)
plt.setp(axs, ylim=custom_ylim)
ii = 0
for sysname in sysnames:
	plotnames = [str(i) for i in range(32)]
	df_arr  = []
	f1		= sysname + '_nu_dp.dat'
	f2		= sysname + '_nu_qp.dat'
	f3		= sysname + '_nu_op.dat'
	d1		= np.loadtxt(f1, dtype=float)
	d2		= np.loadtxt(f2, dtype=float)
	d3		= np.loadtxt(f3, dtype=float)
	lentime = int(len(d1)/32)

	for jj in range(32):
		indexn = np.arange(0, len(d1), 32)
		indexn += jj
		da1 = d1[indexn]
		da2 = d2[indexn]
		da3 = d3[indexn]
		df_arr.append(pd.DataFrame({ 'system' : np.repeat(plotnames[jj], lentime), 'dipole' : da1, 'quadrupole' : da2, 'octupole' : da3}))

	df_mbn = pd.concat(df_arr)
	#dfcheck = df_mbn[df_mbn['system'] == '24']
	#dfcheck['field'].to_csv(sysname + '_test.csv', sep=',', index=False)
	axs[ii].set_title(titlenames[sysname], fontsize=16)
	sns.violinplot(ax=axs[ii], x='system', y='dipole', data=df_mbn, width=0.8, color='yellow', linewidth=1.5, inner=None, saturation=1)
	sns.violinplot(ax=axs[ii], x='system', y='quadrupole', data=df_mbn, width=0.8, color='cyan', linewidth=1.5, inner=None, saturation=1)
	sns.violinplot(ax=axs[ii], x='system', y='octupole', data=df_mbn, width=0.8, color='magenta', linewidth=1.5, inner=None, saturation=1)
	axs[ii].set(xlabel=None, ylabel=None)
	plt.setp(axs[ii].collections, alpha=0.5)
	ii += 1
for ax in axs.flat:
    ax.label_outer()
plt.tight_layout()
fig.subplots_adjust(bottom=0.06, left=0.05)
fig.text(0.5, 0.02, r"Nitrile #", ha='center')
fig.text(0.01, 0.5, r"$\Delta \nu (cm^{-1})$",va='center' ,rotation='vertical')
plt.savefig('nu_space_decomp.png', transparent=True, quality=100)
#!/opt/anaconda3/bin/python3
#-- plot number densities for ferrocene-MBN simulations --
from cProfile import label
from os import system
from turtle import color
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import matplotlib.cm as cm
plt.rcParams.update({'font.sans-serif'	: 'Helvatica',
					'font.family'		: "sans-serif", 
					'font.size'			: 20,
					'font.weight'		: 'regular',
					'xtick.labelsize'	: 16,
					'ytick.labelsize'	: 16,
					'axes.linewidth'	: 1.5})

sysnames		= ['c0-mbn', 'c12-mbn', 'c6-mbn', 'c11-mbn']
plotnames       = {'c6-mbn' : r"$C_{6}H_{12}FEC+4MBN$", 'c11-mbn' : r"$C_{11}H_{22}FEC+4MBN$", 'c12-mbn' : r"$C_{12}H_{25}+4MBN$", 'c0-mbn' : r"$4MBN$", 'c6-mbn-100' : r"$C_{6}H_{12}FEC+4MBN$", 'c11-mbn-100' : r"$C_{11}H_{22}FEC+4MBN$", 'c12-mbn-100' : r"$C_{12}H_{25}+4MBN$", 'c0-mbn-100' : r"$4MBN$"}
colors			= ['blue', 'magenta', 'red', 'lawngreen']


fig, ax1     = plt.subplots(figsize=(9, 6))
plt.setp(ax1, ylim=(0,1.5))

ax1.set_xlabel(r"r (nm)")
ax1.set_ylabel('RDF')
ax2 = ax1.twinx()
ax2.set_ylabel('Number')

for ii in range(len(sysnames)):
	system		= sysnames[ii]
	fname_rdf	= system + '_rdf_NZ_OW.xvg'
	fname_rdf_cn= system + '_rdf_cn_NZ_OW.xvg'
	df_rdf		= pd.read_csv(fname_rdf, header=None, skiprows=25, delim_whitespace=True)
	df_rdf_cn	= pd.read_csv(fname_rdf_cn, header=None, skiprows=25, delim_whitespace=True)
	ax1.plot(df_rdf[0].tolist(), df_rdf[1].tolist(), color=colors[ii], label=plotnames[system], lw=3)
	ax2.plot(df_rdf_cn[0].tolist(), df_rdf_cn[1].tolist(), color=colors[ii], label=plotnames[system], lw=3, linestyle='dotted')
fig.tight_layout()
ax1.legend(fontsize=14, loc='upper right')
plt.savefig('rdf_NZ_OW_22.png', transparent=True, quality=100)
plt.clf()

fig, ax1     = plt.subplots(figsize=(9, 6))
plt.setp(ax1, ylim=(0,1.5))
ax1.set_xlabel(r"r (nm)")
ax1.set_ylabel('RDF')
ax2 = ax1.twinx()
ax2.set_ylabel('Number')

for ii in [2,3]:
	system		= sysnames[ii]
	fname_rdf	= system + '_rdf_FE_OW.xvg'
	fname_rdf_cn= system + '_rdf_cn_FE_OW.xvg'
	df_rdf		= pd.read_csv(fname_rdf, header=None, skiprows=25, delim_whitespace=True)
	df_rdf_cn	= pd.read_csv(fname_rdf_cn, header=None, skiprows=25, delim_whitespace=True)
	ax1.plot(df_rdf[0].tolist(), df_rdf[1].tolist(), color=colors[ii], label=plotnames[system], lw=3)
	ax2.plot(df_rdf_cn[0].tolist(), df_rdf_cn[1].tolist(), color=colors[ii], label=plotnames[system], lw=3, linestyle='dotted')
fig.tight_layout()
ax1.legend(fontsize=14, loc='upper right')
plt.savefig('rdf_FE_OW_22.png', transparent=True, quality=100)
plt.clf()

fig, ax1     = plt.subplots(figsize=(9, 6))
#plt.setp(ax1, ylim=(0,1.5))
ax1.set_xlabel(r"r (nm)")
ax1.set_ylabel('RDF')
ax2 = ax1.twinx()
ax2.set_ylabel('Number')

for ii in [2,3]:
	system		= sysnames[ii]
	fname_rdf	= system + '_rdf_NZ_FE.xvg'
	fname_rdf_cn= system + '_rdf_cn_NZ_FE.xvg'
	df_rdf		= pd.read_csv(fname_rdf, header=None, skiprows=25, delim_whitespace=True)
	df_rdf_cn	= pd.read_csv(fname_rdf_cn, header=None, skiprows=25, delim_whitespace=True)
	ax1.plot(df_rdf[0].tolist(), df_rdf[1].tolist(), color=colors[ii], label=plotnames[system], lw=3)
	ax2.plot(df_rdf_cn[0].tolist(), df_rdf_cn[1].tolist(), color=colors[ii], label=plotnames[system], lw=3, linestyle='dotted')
fig.tight_layout()
ax1.legend(fontsize=14, loc='upper right')
plt.savefig('rdf_NZ_FE_22.png', transparent=True, quality=100)
plt.clf()
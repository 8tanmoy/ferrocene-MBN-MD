#!/opt/anaconda3/bin/python3
#-- plot number densities for ferrocene-MBN simulations --

from os import system
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns

plt.rcParams.update({'font.sans-serif'	: 'Helvatica',
					'font.family'		: "sans-serif", 
					'font.size'			: 20,
					'font.weight'		: 'regular',
					'xtick.labelsize'	: 16,
					'ytick.labelsize'	: 16,
					'axes.linewidth'	: 1.5})

#--load files--
#['c0-mbn', 'c6-mbn', 'c11-mbn', 'c12-mbn', 'c0-mbn-100', 'c6-mbn-100', 'c11-mbn-100', 'c12-mbn-100']
sysnames	= ['c6-mbn', 'c11-mbn', 'c12-mbn', 'c0-mbn']
plotnames	= {'c6-mbn' : r"$C_{6}H_{12}FEC+4MBN$", 'c11-mbn' : r"$C_{11}H_{22}FEC+4MBN$", 'c12-mbn' : r"$C_{12}H_{25}+4MBN$", 'c0-mbn' : r"$4MBN$"}
#dfs         = {}

fig, axs = plt.subplots(sharex=True, sharey=True)
fig.set_figwidth(8)
fig.set_figheight(6)

for sysname in sysnames:
    fname = sysname + '_hist.xvg'
    df = pd.read_csv(fname, skiprows=24, header=None, delim_whitespace=True, names=['Angle (degrees)', 'Probability'])
    sns.lineplot(x='Angle (degrees)', y='Probability', data=df, label=plotnames[sysname])
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig('gangle_dist.png')
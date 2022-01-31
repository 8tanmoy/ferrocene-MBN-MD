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
fig.set_figwidth(12)
fig.set_figheight(6)
my_xlim = 50
plt.xlim(0,my_xlim)

for sysname in sysnames:
    fname = sysname + '_nu_acf.dat'
    df = pd.read_csv(fname, header=0)
    sns.lineplot(x='time', y='nu_inter_acf', data=df, label=plotnames[sysname])
plt.hlines(y=0, xmin=0, xmax=my_xlim, color='black')
plt.legend(fontsize=14)
plt.xlabel(r"$\tau$")
plt.ylabel(r"$<\delta \nu (0) \cdot \delta \nu (t)>$")
plt.tight_layout()
plt.savefig('nu_acf_long.png', transparent=True)
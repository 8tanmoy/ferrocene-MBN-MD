from locale import D_FMT
from turtle import width
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
plt.rcParams.update({'font.sans-serif'	: 'Helvatica',
					'font.family'		: "sans-serif", 
					'font.size'			: 20,
					'font.weight'		: 'regular',
					'xtick.labelsize'	: 16,
					'ytick.labelsize'	: 16,
					'axes.linewidth'	: 1.5})

fig, ax = plt.subplots(figsize=(8, 7))

sysnames = ['c0-mbn-100', 'c12-mbn-100', 'c6-mbn-100', 'c11-mbn-100']
plotnames	= {'c6-mbn-100' : r"$C_{6}H_{12}FEC$"+'\n+4MBN', 'c11-mbn-100' : r"$C_{11}H_{22}FEC$"+'\n+4MBN', 'c12-mbn-100' : r"$C_{12}H_{25}$"+'\n+4MBN', 'c0-mbn-100' : r"$4MBN$"}
df_arr  = []

for sysname in sysnames:
    fname   = sysname + '_nu_inter.dat'
    data    = np.loadtxt(fname, dtype=float)
    mean    = np.mean(data)
    print(sysname, mean)
    df_arr.append(pd.DataFrame({ 'system' : np.repeat(plotnames[sysname], len(data)), 'field' : data, 'mean' : mean}))
df_mbn = pd.concat(df_arr)

plt.ylim(-40, 40)
#sns.violinplot(ax=ax, x='system', y='field', data=df)
plt.axhline(y=0, color='black', lw=0.5)
sns.boxplot(ax=ax, x='system', y='field', data=df_mbn, width=0.5, linewidth=1.5, color='yellow', saturation=1)
sns.pointplot(x='system', y='mean', data=df_mbn, join=True, color='black', facecolors='none', markersize=10, linewidth=1)
ax.set(xlabel='system', ylabel=r"$\Delta \nu (cm^{-1})$")
fig.tight_layout()
plt.savefig('field_mbn_100_box.png', transparent=True, quality=100)
plt.clf()

fig, ax = plt.subplots(figsize=(8, 7))
plt.ylim(-40, 40)
#sns.violinplot(ax=ax, x='system', y='field', data=df)
plt.axhline(y=0, color='black', lw=0.5)
sns.violinplot(ax=ax, x='system', y='field', data=df_mbn, width=0.5, linewidth=1.5, color='yellow', saturation=1)
sns.pointplot(x='system', y='mean', data=df_mbn, join=True, color='black', facecolors='none', markersize=10, linewidth=1)
ax.set(xlabel='system', ylabel=r"$\Delta \nu (cm^{-1})$")
fig.tight_layout()
plt.savefig('field_mbn_100_violin.png', transparent=True, quality=100)
plt.clf()
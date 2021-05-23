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

sysnames = ['c0-mbn', 'c12-mbn', 'c6-mbn', 'c11-mbn']
plotnames	= {'c6-mbn' : r"$C_{6}H_{12}FEC$"+'\n+4MBN', 'c11-mbn' : r"$C_{11}H_{22}FEC$"+'\n+4MBN', 'c12-mbn' : r"$C_{12}H_{25}$"+'\n+4MBN', 'c0-mbn' : r"$4MBN$"}
df_arr  = []

for sysname in sysnames:
    fname   = sysname + '_field_inter_mbn.dat'
    data    = np.loadtxt(fname, dtype=float)
    df_arr.append(pd.DataFrame({ 'system' : np.repeat(plotnames[sysname], len(data)), 'field' : data}))
df_mbn = pd.concat(df_arr)

plt.ylim(-10, 20)
#sns.violinplot(ax=ax, x='system', y='field', data=df)
sns.boxplot(ax=ax, x='system', y='field', data=df_mbn, width=0.5)
ax.set(xlabel='system', ylabel=r"$F_{CN} \: ( V\:nm^{-1} )$")
fig.tight_layout()
plt.savefig('field_mbn_22_box.png', transparent=True, quality=100)
plt.clf()

#-------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 7))

df_arr  = []
for sysname in sysnames:
    fname   = sysname + '_field_inter_nombn.dat'
    data    = np.loadtxt(fname, dtype=float)
    df_arr.append(pd.DataFrame({ 'system' : np.repeat(plotnames[sysname], len(data)), 'field' : data}))
df_nombn = pd.concat(df_arr)

plt.ylim(-10, 20)
#sns.violinplot(ax=ax, x='system', y='field', data=df)
sns.boxplot(ax=ax, x='system', y='field', data=df_nombn, width=0.5)
ax.set(xlabel='system', ylabel=r"$F_{CN} \: ( V\:nm^{-1} )$")
fig.tight_layout()
plt.savefig('field_nombn_22_box.png', transparent=True, quality=100)
plt.clf()
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
	f1		= sysname + '_nu_dp.dat'
	f2		= sysname + '_nu_qp.dat'
	f3		= sysname + '_nu_op.dat'
	d1		= np.loadtxt(f1, dtype=float)
	d2		= np.loadtxt(f2, dtype=float)
	d3		= np.loadtxt(f3, dtype=float)
	df_arr.append(pd.DataFrame({ 'system' : np.repeat(plotnames[sysname], len(d1)), 'dipole' : d1, 'qpole' : d2, 'opole' : d3}))
df_mbn = pd.concat(df_arr)

plt.ylim(-40, 40)
#sns.violinplot(ax=ax, x='system', y='field', data=df)
plt.axhline(y=0, color='black', lw=0.5)
sns.violinplot(ax=ax, x='system', y='dipole', data=df_mbn, width=0.5, color='yellow', linewidth=1.5, inner=None, saturation=1)
sns.violinplot(ax=ax, x='system', y='qpole', data=df_mbn, width=0.5, color='cyan', linewidth=1.5, inner=None, saturation=1)
sns.violinplot(ax=ax, x='system', y='opole', data=df_mbn, width=0.5, color='magenta', linewidth=1.5, inner=None, saturation=1)
ax.set(xlabel='system', ylabel=r"$\Delta \nu (cm^{-1})$")
plt.setp(ax.collections, alpha=0.5)
fig.tight_layout()
plt.savefig('nu_npole.png', transparent=True, quality=100)
plt.clf()
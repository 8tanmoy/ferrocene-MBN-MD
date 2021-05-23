from locale import D_FMT
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

fig, ax = plt.subplots(figsize=(14, 7))

sysnames = ['c0-mbn', 'c12-mbn', 'c6-mbn', 'c11-mbn', 'c0-mbn-100',  'c12-mbn-100', 'c6-mbn-100', 'c11-mbn-100']
df_arr  = []
for sysname in sysnames:
    fname   = sysname + '_field_inter_mbn.dat.dat'
    data    = np.loadtxt(fname, dtype=float)
    df_arr.append(pd.DataFrame({ 'system' : np.repeat(sysname, len(data)), 'field' : data}))
df = pd.concat(df_arr)
#print(df.describe())

#plot violin chart
plt.ylim(-10, 20)
sns.violinplot(ax=ax, x='system', y='field', data=df)
#sns.boxplot(ax=ax, x='system', y='field', data=df)
ax.set(xlabel='system', ylabel=r"$F_{CN} \: ( V\:nm^{-1} )$")
#plt.savefig('field_box.png', transparent=True, quality=100)
plt.savefig('field_violin.png', transparent=True, quality=100)
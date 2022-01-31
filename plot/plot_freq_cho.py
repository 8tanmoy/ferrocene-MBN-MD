from matplotlib import markers
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
plt.rcParams.update({'font.sans-serif'	: 'Helvatica',
					'font.family'		: 'sans-serif', 
					'font.size'			: 20,
					'font.weight'		: 'regular',
					'xtick.labelsize'	: 16,
					'ytick.labelsize'	: 16,
					'axes.linewidth'	: 2})

sysnames22      = ['c0-mbn', 'c12-mbn', 'c6-mbn', 'c11-mbn']
sysnames100     = ['c0-mbn-100', 'c12-mbn-100', 'c6-mbn-100', 'c11-mbn-100']  
plotnames       = {'c6-mbn' : r"$C_{6}H_{12}FEC$"+'\n+4MBN', 'c11-mbn' : r"$C_{11}H_{22}FEC$"+'\n+4MBN', 'c12-mbn' : r"$C_{12}H_{25}$"+'\n+4MBN', 'c0-mbn' : r"$4MBN$", 'c6-mbn-100' : r"$C_{6}H_{12}FEC$"+'\n+4MBN', 'c11-mbn-100' : r"$C_{11}H_{22}FEC$"+'\n+4MBN', 'c12-mbn-100' : r"$C_{12}H_{25}$"+'\n+4MBN', 'c0-mbn-100' : r"$4MBN$"}

shift_mean_mbn  = []
dummy           = [plotnames[sysname] for sysname in sysnames22]

fig, ax     = plt.subplots(figsize=(7, 6))

nu_100      = [-8.61, -15.65, -15.22, -12.39]
nu_75		= [-5.01, -9.67, -12.11, -8.77]
nu_50       = [-3.19, -7.99, -8.88, -8.29]
nu_32       = [-2.34, -5.11, -5.88, -6.19]

plt.ylim(-20, 0)
plt.plot(dummy, nu_100, marker="o", color='black', label=r'$\sigma=6.25nm^{-2}$')
plt.plot(dummy, nu_75, marker="o", color='brown', label=r'$\sigma=4.68nm^{-2}$')
plt.plot(dummy, nu_50, marker="o", color='red', label=r'$\sigma=3.12nm^{-2}$')
plt.plot(dummy, nu_32, marker="o", color='orange', label=r'$\sigma=2nm^{-2}$')
plt.legend(loc='upper right', fontsize=14)
ax.set(xlabel='system', ylabel=r"$\Delta \nu (cm^{-1})$")
fig.tight_layout()
plt.savefig('nu_density.png', transparent=True, quality=100)

from curses import nl
from random import gauss
from haiku import transparent
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys


plt.rcParams.update({'font.sans-serif'  : 'Helvatica',
                    'font.family'       : "sans-serif",
                    'font.size'         : 16,
                    'font.weight'       : 'regular',
                    'xtick.labelsize'   : 16,
                    'ytick.labelsize'   : 16,
                    'axes.labelsize'    : 20,
                    'axes.linewidth'    : 1.5,
                    'legend.fontsize'   : 11,
                    'legend.loc'        : 'upper right'})

nlig    = 32
dfs     = []

angmax  = []
dfs_avg = []
angavg  = []

for i in range(nlig):
    df_hist = pd.read_csv(f'hist_{i}.xvg', header=None, delim_whitespace=True, skiprows=24, names=['angle', 'probability'])
    df_hist['idx'] = int(i)

    df_avg = pd.read_csv(f'ave_{i}.xvg', header=None, delim_whitespace=True, skiprows=24, names=['time', 'angle'])
    df_avg['idx'] = int(i)
    del df_avg['time']
    #print(df_avg)

    # correct angles for the flipped plane
    if i < (nlig//2):
        df_hist['angle']    = 180.0 - df_hist['angle']
        df_avg['angle']     = 180.0 - df_avg['angle']
    angmax.append(df_hist[df_hist['probability']==np.max(df_hist['probability'].to_numpy())]['angle'].values.mean())
    angavg.append(df_avg['angle'].mean())
    dfs.append(df_hist)
    dfs_avg.append(pd.DataFrame({'idx': int(i), 'angle' : df_avg['angle']}))
dfs     = pd.concat(dfs)

idx_means   = [[i, dfs_avg[i]['angle'].mean()] for i in range(len(dfs_avg))]
idx_means.sort(key=lambda row: row[1])
sort_order  = [idx_means[i][0] for i in range(len(idx_means))]

dfs_avg = pd.concat(dfs_avg)
print(dfs)
print(dfs_avg)
print(len(df_avg))

#-- get maxima (mode) position and write list --
angmax          = np.array(angmax).flatten()
idx             = np.arange(0, nlig, 1).astype(int)

idx_angmax_zipped   = np.array(list(zip(idx, angmax)))
idx_angavg_zipped   = np.array(list(zip(idx, angavg)))

np.savetxt('angmax.dat', idx_angmax_zipped, delimiter=',')
np.savetxt('angavg.dat', idx_angavg_zipped, delimiter=',')

#-- plotting --
fig, ax = plt.subplots(figsize=(6,5))
ax.set_xlim(0, 150)
#plt.axvline(x=angmean[0], ymin=0, ymax=1.0, color='blue')
sns.lineplot(data=dfs[(dfs['idx']==0)], x='angle', y='probability', color='black', label='idx 0', ax=ax)
sns.lineplot(data=dfs[(dfs['idx']==9)], x='angle', y='probability', color='red', label='idx 9', ax=ax)

p = sns.lineplot(data=dfs.reset_index(), x='angle', y='probability',
    hue='idx', alpha=0.15, palette=sns.color_palette("Blues", as_cmap=True)
    )
ax.set_xlabel(r"angle of $\vec{CN}$ and $\vec{Z} (\degree)$")
plt.tight_layout()
plt.savefig('all_anghist_z_corrected.png', dpi=200, transparent=True)


plt.clf()
fig, ax = plt.subplots(figsize=(12,5))
plt.ylim(0, 150)
plt.axhline(y=min(angavg), xmin=0, xmax=31, alpha=0.2, color='black')
plt.axhline(y=max(angavg), xmin=0, xmax=31, alpha=0.2, color='black')
box = sns.boxplot(data=dfs_avg, x='idx', y='angle', ax=ax, color='white', fliersize=0.5, boxprops=dict(alpha=1.0), width=0.5, 
    order=sort_order)
box.set(xlabel=r"Nitrile index", ylabel=r"angle of $\vec{CN}$ and $\vec{Z}$")
angavg_ordered = [angavg[i] for i in sort_order]
print(sort_order)
print(angavg_ordered)
plt.scatter(idx, angavg_ordered, s=20, color='red', label=r"<angle of $\vec{CN}$ and $\vec{Z}$>")
plt.xticks(sort_order, rotation=90)
plt.legend()
plt.tight_layout()
plt.savefig('all_angavg_z_corrected.png', dpi=200, transparent=True)

import plotly.express as px
fig = px.line(dfs, x='angle', y='probability', color='idx')
fig.update_traces(line=dict(width=4.0))
fig.write_html('all_anghist_z_corrected.html')

#== calculate kde of angles
from scipy.stats import gaussian_kde
from scipy.signal import find_peaks
data = dfs_avg['angle'].to_numpy()
kde = gaussian_kde(data)
angrange    = np.arange(0, 180, 0.01)
kde_eval    = kde.evaluate(angrange)
x = find_peaks(kde_eval)
peak1, peak2 = x[0]
peak1=int(peak1)
peak2=int(peak2)
angmin      = angrange[peak1 + np.argmin(kde_eval[peak1:peak2])]

plt.clf()
plt.plot(angrange, kde_eval)
plt.axvline(x=angrange[peak1], ymin=0.0, ymax=1.0, color='red')
plt.axvline(x=angrange[peak2], ymin=0.0, ymax=1.0, color='red')
plt.axvline(x=angmin, ymin=0.0, ymax=1.0, color='red')
plt.savefig('kde.png')

print(len(data))
frac_standing   = len(data[data < angmin])/len(data)
print(frac_standing)
mean_of_standing = np.mean(data[data < angmin])
std_of_standing  = np.std(data[data < angmin])
print('mean, std', mean_of_standing, std_of_standing)
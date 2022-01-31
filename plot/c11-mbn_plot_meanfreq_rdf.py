from numpy.lib.index_tricks import r_
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.signal import savgol_filter

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

fig, axs = plt.subplots(3,1, figsize=(8, 12), sharex=True, sharey=False)

sysname     = 'c11-mbn'
#==== get derivative of RDF and get dip position ====
idx_nz      = [2013, 2026, 2039, 2052, 2065, 2078, 2091, 2104, 2117, 2130, 2143, 2156, 2169, 2182, 2195,
2208, 5085, 5098, 5111, 5124, 5137, 5150, 5163, 5176, 5189, 5202, 5215, 5228, 5241, 5254,
5267, 5280]

serial_idx      = []
r_rdf_dip       = []
nwat_rdf_dip    = []

for ii in range(len(idx_nz)):
    fname       = f"{sysname}_rdf_resid/rdf_NZ_OW_{idx_nz[ii]}.xvg"
    df1         = pd.read_csv(fname, header=None, delim_whitespace=True, skiprows=25, names=['r(nm)', 'RDF'])
    arr_r       = df1['r(nm)'].to_numpy()
    arr_rdf     = df1['RDF'].to_numpy()
    arr_rdf_max_idx = np.argmax(arr_rdf)
    arr_rdf_min_idx = arr_rdf_max_idx + np.argmin(arr_rdf[arr_rdf_max_idx:])

    axs[0].plot(arr_r, arr_rdf, color='blue')                               #just plot rdf
    #axs[0].vlines(arr_r[arr_rdf_max_idx], ymin=0.0, ymax=1.0, color='red') #plot maxima
    axs[0].vlines(arr_r[arr_rdf_min_idx], ymin=0.0, ymax=1.0, color='red')  #plot minima after maxima

#==== get integrated RDF at dip ====
    fname       = f"{sysname}_rdf_resid/rdf_cn_NZ_OW_{idx_nz[ii]}.xvg"
    df1         = pd.read_csv(fname, header=None, delim_whitespace=True, skiprows=25, names=['r(nm)', 'RDF_cn'])
    arr_r       = df1['r(nm)'].to_numpy()
    arr_rdf_cn  = df1['RDF_cn'].to_numpy()

    axs[1].plot(arr_r, arr_rdf_cn, color='blue')
    axs[1].vlines(arr_r[arr_rdf_min_idx], ymin=0.0, ymax=400, color='red')
    #axs[1].text(arr_r[arr_rdf_min_idx], arr_rdf_cn[arr_rdf_min_idx] + 100, f'#wat = {arr_rdf_cn[arr_rdf_min_idx]}')

    #-- filter for eliminating minima positions beyond 0.5 nm --
    if arr_r[arr_rdf_min_idx] < 0.5:
        serial_idx.append(ii)
        r_rdf_dip.append(arr_r[arr_rdf_min_idx])
        nwat_rdf_dip.append(arr_rdf_cn[arr_rdf_min_idx])

        axs[2].plot(arr_r, arr_rdf, color='blue')
        axs[2].vlines(arr_r[arr_rdf_min_idx], ymin=0.0, ymax=1.0, color='black')

plt.savefig(f'{sysname}_rdf_nwat.png', transparent=True, dpi=200)

#r_min_mean  = np.max(r_rdf_dip)
r_min_mean  = 0.5
r_min_idx   = int(r_min_mean / 0.005)
print(f'mean of well behaved rdfs dip: {r_min_mean} and check {arr_r[r_min_idx]}')

nwat_rdf_dip_all    = []
for ii in range(len(idx_nz)):
    fname       = f"{sysname}_rdf_resid/rdf_cn_NZ_OW_{idx_nz[ii]}.xvg"
    df1         = pd.read_csv(fname, header=None, delim_whitespace=True, skiprows=25, names=['r(nm)', 'RDF_cn'])
    arr_rdf_cn  = df1['RDF_cn'].to_numpy()
    nwat_rdf_dip_all.append(arr_rdf_cn[r_min_idx])

plt.clf()
fig, ax = plt.subplots(figsize=(6, 5), sharex=True, sharey=True)
plt.ylim(-20,20)
#==== get mean of filtered field ====
mean_freq  = []

fname       = sysname + '_nu_inter.dat'
data        = np.loadtxt(fname, dtype=float)
df2         = pd.DataFrame({'freq' : data})
idx         = np.array([np.arange(0, 32, 1)] * 20_000).flatten()
df2['idx']  = idx
df2_mean    = df2.groupby(['idx']).mean()

for jj in serial_idx:
    mean_freq.append(df2_mean.iloc[jj]['freq'])

#-- combine serial, r, and integrated rdf in df --
df          = pd.DataFrame({'serial' : serial_idx, 'r(nm)' : r_rdf_dip, 'num_wat' : nwat_rdf_dip, 'mean_freq': mean_freq})
df_all      = pd.DataFrame({'serial' : np.array(np.arange(0, 32, 1)), 'num_wat' : nwat_rdf_dip_all, 'mean_freq' : df2_mean['freq']})
print(df)
print(df_all)
meanwat     = df_all['num_wat'].mean()
print(f'average number of water within first solvation shell: {meanwat}')

#=== plot stuff ====
ax.set_xlabel(r"$N_{water}$ " + f' for r < {arr_r[r_min_idx]} nm')
ax.set_ylabel(r"$\Delta \nu$")

ax.scatter(df_all['num_wat'], df_all['mean_freq'], marker='o', color='black')
ax.scatter([df_all['num_wat'][i] for i in df['serial'].to_list()], [df_all['mean_freq'][i] for i in df['serial'].to_list()], marker='o', color='red', s=150, alpha=0.3, label='well-behaved RDF')

reg = sns.regplot(x='num_wat', y='mean_freq', data=df_all, ax=ax)
reg.set(xlabel=r"$N_{water}$ " + f' for r < {arr_r[r_min_idx]} nm', ylabel=r"$\Delta \nu$")
result = stats.linregress(df_all['num_wat'], df_all['mean_freq'])
print(f'slope:\t{result.slope}\n intercept:\t{result.intercept}\n r_value:\t{result.rvalue}\n p_value:\t{result.pvalue}\n std_err:\t{result.stderr}')
print(f" R-squared:\t{result.rvalue**2:.6f}\n")
plt.legend()
plt.text(6, 10, r"$R^2=$" + f"{result.rvalue**2:.2f}\n")
plt.tight_layout()
plt.savefig(f'{sysname}_meanfreq_rdf.png', transparent=True, dpi=200)

#== load angmax data
angavg_data = np.loadtxt(f'{sysname}_gangle/angavg.dat', delimiter=',')
angavg_data = angavg_data[:,1]
#== plot another figure with freq vs angmax, nwat vs angmax
plt.clf()
fig, axs = plt.subplots(2,1, figsize=(6, 9), sharex=True, sharey=False)
plt.xlim(0, 125)
axs[0].set_ylim(-20, 20)
axs[0].set_xlabel(r"<angle of $\vec{CN}$ with $\vec{Z}$> ($\degree$)")
axs[1].set_xlabel(r"<angle of $\vec{CN}$ with $\vec{Z}$> ($\degree $)")

axs[0].scatter(angavg_data, df_all['mean_freq'], marker='o', color='black')
axs[0].scatter([angavg_data[i] for i in df['serial'].to_list()], df['mean_freq'], marker='o', color='red', s=150, alpha=0.3, label='well-behaved RDF')
axs[0].set_ylabel(r"$\Delta \nu$")
axs[0].legend()

axs[1].scatter(angavg_data, df_all['num_wat'], marker='o', color='black')
axs[1].scatter([angavg_data[i] for i in df['serial'].to_list()], [df_all['num_wat'][i] for i in df['serial'].to_list()], marker='o', color='red', s=150, alpha=0.3, label='well-behaved RDF')
axs[1].set_ylabel(r"$N_{water}$ " + f'at r < {arr_r[r_min_idx]} nm')
plt.tight_layout()
plt.savefig(f'{sysname}_meanfreq_angavg.png', transparent=True, dpi=200)
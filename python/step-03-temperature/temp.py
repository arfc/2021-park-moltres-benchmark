import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
sys.path.append(
        os.path.dirname(
                os.path.dirname(
                        os.path.abspath(__file__))))
from common_func import get_disc, get_benchmark_ave_disc

# Data
aa = pd.read_csv('temp_csv_aa_0002.csv')
bb = pd.read_csv('temp_csv_bb_0002.csv')
benchmark_aa = pd.read_csv('T_AA', delim_whitespace=True, header=None)
benchmark_bb = pd.read_csv('T_BB', delim_whitespace=True, header=None)

# Calculate % discrepancy
disc_aa = get_disc(aa['temp'], benchmark_aa)
disc_bb = get_disc(bb['temp'], benchmark_bb)

ave_aa = get_benchmark_ave_disc(benchmark_aa)
ave_bb = get_benchmark_ave_disc(benchmark_bb)

f = open('temp.txt', 'w')
f.write("Discrepancy in temperature along AA' = " +
        str(disc_aa*100) + " %\n")
f.write("Discrepancy in temperature along BB' = " +
        str(disc_bb*100) + " %\n")
f.write("Benchmark average discrepancy in temperature along AA' = " +
        str(ave_aa*100) + " %\n")
f.write("Benchmark average discrepancy in temperature along BB' = " +
        str(ave_bb*100) + " %\n")
f.close()

# %% Plot
y = np.linspace(0, 2, 201)
code = ['CNRS-SP1', 'CNRS-SP3', 'Polimi-Diff', 'PSI-Diff', 'TUD-S2', 'TUD-S6']

plt.rc('font', size=12)          # controls default text sizes
plt.rc('axes', titlesize=12)     # fontsize of the axes title
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=11)    # fontsize of the tick labels
plt.rc('ytick', labelsize=11)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize
plt.rc('figure', titlesize=12)  # fontsize of the figure title

fig, ax = plt.subplots(figsize=[6, 5])
ax.plot(bb['temp'], y, label='Moltres', color='tab:blue')
ax.plot(benchmark_bb[:][2], y, label='CNRS-SP$_3$', color='tab:orange',
        linestyle='--')
ax.plot(benchmark_bb[:][3], y, label='Polimi', color='tab:green',
        linestyle=':')
ax.plot(benchmark_bb[:][4], y, label='PSI', color='tab:red',
        linestyle='-.')
ax.plot(benchmark_bb[:][6], y, label='TUD-S$_6$', color='tab:cyan',
        linestyle=(0, (3, 1, 1, 1, 1, 1)))
ax.legend()
ax.grid(which='both')
ax.set_xlim(900, 1350)
ax.set_ylim(0, 2)
ax.set_xlabel(r'$T$ [K]')
ax.set_ylabel(r'$y$ [m]')
plt.savefig('0-3-temp-plot.png', dpi=400)

ax.set_xlim(900, 1100)
ax.set_ylim(1.94, 2)
plt.savefig('0-3-temp-plot-zoom.png', dpi=400)

# %% Write tsv

coords = np.linspace(0, 2, 201)
aa_df = pd.DataFrame({'x (m)': np.around(coords, decimals=2),
                      'temperature (K)': aa['temp']})
bb_df = pd.DataFrame({'y (m)': np.around(coords, decimals=2),
                      'temperature (K)': bb['temp']})
aa_df.to_csv('moltres_0.3_AA', index=False, sep='\t')
bb_df.to_csv('moltres_0.3_BB', index=False, sep='\t')

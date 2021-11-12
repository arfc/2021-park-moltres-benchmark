import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
sys.path.append(
        os.path.dirname(
                os.path.dirname(
                        os.path.abspath(__file__))))
from common_func import get_disc, get_benchmark_disc

# Data
aa = pd.read_csv('nts_csv_aa_0002.csv')
benchmark_aa = pd.read_csv('fiss_dens_AA', delim_whitespace=True, header=None)

# Fission cross section data
sigmaf = [1.11309e-03, 1.08682e-03, 1.52219e-03,
          2.58190e-03, 5.36326e-03, 1.44917e-02]

# Pre-multiply with appropriate group fission XS and sum at each position
fiss = np.zeros(201)
for i in range(6):
    group = 'group' + str(i+1)
    fiss += np.array(aa[group] * sigmaf[i]) * 1e6

# Calculate % discrepancy
disc_aa = get_disc(fiss, benchmark_aa)

ave_aa, std_aa = get_benchmark_disc(benchmark_aa)

f = open('fission-rate.txt', 'w')
f.write("Discrepancy in fission rate along AA' = " +
        str(disc_aa*100) + " %\n")
f.write("Benchmark average discrepancy in fission rate along AA' = " +
        str(ave_aa*100) + " %\n")
f.write("Benchmark discrepancy std dev in fission rate along AA' = " +
        str(std_aa*100) + " %\n")
f.close()

# %% Plot
x = np.linspace(0, 2, 201)
code = ['CNRS-SP1', 'CNRS-SP3', 'Polimi-Diff', 'PSI-Diff', 'TUD-S2', 'TUD-S6']

plt.rc('font', size=12)          # controls default text sizes
plt.rc('axes', titlesize=12)     # fontsize of the axes title
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=11)    # fontsize of the tick labels
plt.rc('ytick', labelsize=11)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize
plt.rc('figure', titlesize=12)  # fontsize of the figure title

fig, ax = plt.subplots(figsize=[6, 5])
ax.plot(x, fiss, label='Moltres', color='tab:blue')
ax.plot(x, benchmark_aa[:][2], label='CNRS-SP$_3$', color='tab:orange',
        linestyle='--')
ax.plot(x, benchmark_aa[:][3], label='Polimi', color='tab:green',
        linestyle=':')
ax.plot(x, benchmark_aa[:][4], label='PSI', color='tab:red',
        linestyle='-.')
ax.plot(x, benchmark_aa[:][6], label='TUD-S$_6$', color='tab:cyan',
        linestyle=(0, (3, 1, 1, 1, 1, 1)))
ax.legend()
ax.grid(which='both')
ax.set_xlim(0, 2)
ax.set_ylim(0, 2e19)
ax.set_xlabel(r'$x$ [m]')
ax.set_ylabel(r'Fission rate density [m$^{-3}\cdot$s$^{-1}$]')
plt.savefig('0-2-fiss-plot.png', dpi=400)

# %% Write tsv

coords = np.linspace(0, 2, 201)
aa_df = pd.DataFrame({'x (m)': np.around(coords, decimals=2),
                      'fiss dens (1/m3s)': fiss})
aa_df.to_csv('moltres_0.2_AA', index=False, sep='\t')

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
sys.path.append(
        os.path.dirname(
                os.path.dirname(
                        os.path.abspath(__file__))))
from common_func import get_disc, get_benchmark_disc    # noqa: E402

# Data
flux_aa = pd.read_csv('power-coupling_csv_flux_aa_0003.csv')
flux_bb = pd.read_csv('power-coupling_csv_flux_bb_0003.csv')
temp_aa = pd.read_csv('power-coupling_csv_temp_aa_0003.csv')
temp_bb = pd.read_csv('power-coupling_csv_temp_bb_0003.csv')
data = pd.read_csv('../step-02-neutronics/nts_csv_aa_0002.csv')

benchmark_aa_fiss = pd.read_csv('delta_fiss_dens_AA',
                                delim_whitespace=True,
                                header=None)
benchmark_bb_fiss = pd.read_csv('delta_fiss_dens_BB',
                                delim_whitespace=True,
                                header=None)
benchmark_aa_temp = pd.read_csv('T_AA', delim_whitespace=True, header=None)
benchmark_bb_temp = pd.read_csv('T_BB', delim_whitespace=True, header=None)

# %%    Fission rate density

# Fission cross section
sigmaf = [1.11309e-03, 1.08682e-03, 1.52219e-03,
          2.58190e-03, 5.36326e-03, 1.44917e-02]

# Pre-multiply with appropriate group fission XS and sum at each position
sigmaf_aa = np.zeros((6, 201))
sigmaf_bb = np.zeros((6, 201))
for i in range(6):
    for j in range(201):
        sigmaf_aa[i, j] = sigmaf[i] * (1 - 2e-4 * (temp_aa['temp'][j]-900))
        sigmaf_bb[i, j] = sigmaf[i] * (1 - 2e-4 * (temp_bb['temp'][j]-900))

fiss_aa = np.zeros(201)
fiss_bb = np.zeros(201)
for i in range(6):
    group = 'group' + str(i+1)
    fiss_aa += np.array(
            (flux_aa[group] * sigmaf_aa[i, ] - data[group] * sigmaf[i])
                ) * 1e6
    fiss_bb += np.array(
            (flux_bb[group] * sigmaf_bb[i, ] - data[group] * sigmaf[i])
                ) * 1e6

# Calculate % discrepancy
disc_aa_fiss = get_disc(fiss_aa, benchmark_aa_fiss)
disc_bb_fiss = get_disc(fiss_bb, benchmark_bb_fiss)
disc_aa_temp = get_disc(temp_aa['temp'], benchmark_aa_temp)
disc_bb_temp = get_disc(temp_bb['temp'], benchmark_bb_temp)

ave_aa_fiss, std_aa_fiss = get_benchmark_disc(benchmark_aa_fiss)
ave_bb_fiss, std_bb_fiss = get_benchmark_disc(benchmark_bb_fiss)
ave_aa_temp, std_aa_temp = get_benchmark_disc(benchmark_aa_temp)
ave_bb_temp, std_bb_temp = get_benchmark_disc(benchmark_bb_temp)

f = open('power-coupling.txt', 'w')
f.write("Discrepancy in fission rate along AA' = " +
        str(disc_aa_fiss*100) + " %\n")
f.write("Discrepancy in fission rate along BB' = " +
        str(disc_bb_fiss*100) + " %\n")
f.write("Discrepancy in temperature along AA' = " +
        str(disc_aa_temp*100) + " %\n")
f.write("Discrepancy in temperature along BB' = " +
        str(disc_bb_temp*100) + " %\n")
f.write("Benchmark average discrepancy in fission rate along AA' = " +
        str(ave_aa_fiss*100) + " %\n")
f.write("Benchmark average discrepancy in fission rate along BB' = " +
        str(ave_bb_fiss*100) + " %\n")
f.write("Benchmark average discrepancy in temperature along AA' = " +
        str(ave_aa_temp*100) + " %\n")
f.write("Benchmark average discrepancy in temperature along BB' = " +
        str(ave_bb_temp*100) + " %\n")
f.write("Benchmark discrepancy std dev in fission rate along AA' = " +
        str(std_aa_fiss*100) + " %\n")
f.write("Benchmark discrepancy std dev in fission rate along BB' = " +
        str(std_bb_fiss*100) + " %\n")
f.write("Benchmark discrepancy std dev in temperature along AA' = " +
        str(std_aa_temp*100) + " %\n")
f.write("Benchmark discrepancy std dev in temperature along BB' = " +
        str(std_bb_temp*100) + " %\n")
f.close()

# Plot
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
ax.plot(x, temp_aa['temp'], label='Moltres', color='tab:blue')
ax.plot(x, benchmark_aa_temp[:][2], label='CNRS-SP$_3$', color='tab:orange',
        linestyle='--')
ax.plot(x, benchmark_aa_temp[:][3], label='Polimi', color='tab:green',
        linestyle=':')
ax.plot(x, benchmark_aa_temp[:][4], label='PSI', color='tab:red',
        linestyle='-.')
ax.plot(x, benchmark_aa_temp[:][6], label='TUD-S$_6$', color='tab:cyan',
        linestyle=(0, (3, 1, 1, 1, 1, 1)))
ax.legend()
ax.grid(which='both')
ax.set_xlim(0, 2)
ax.set_ylim(900, 1400)
ax.set_xlabel(r'$x$ [m]')
ax.set_ylabel(r'$T$ [K]')
plt.savefig('1-2-temp-plot.png', dpi=400)

fig, ax = plt.subplots(figsize=[6, 5])
ax.plot(x, fiss_aa, label='Moltres', color='tab:blue')
ax.plot(x, benchmark_aa_fiss[:][2], label='CNRS-SP$_3$', color='tab:orange',
        linestyle='--')
ax.plot(x, benchmark_aa_fiss[:][3], label='Polimi', color='tab:green',
        linestyle=':')
ax.plot(x, benchmark_aa_fiss[:][4], label='PSI', color='tab:red',
        linestyle='-.')
ax.plot(x, benchmark_aa_fiss[:][6], label='TUD-S$_6$', color='tab:cyan',
        linestyle=(0, (3, 1, 1, 1, 1, 1)))
ax.legend()
ax.grid(which='both')
ax.set_xlim(0, 2)
ax.set_ylim(-1e18, 6e17)
ax.set_xlabel(r'$x$ [m]')
ax.set_ylabel(r'Change in fission rate density [m$^{-3}\cdot$s$^{-1}$]')
plt.savefig('1-2-fiss-plot.png', dpi=400)

# %% Write tsv

coords = np.linspace(0, 2, 201)
aa_df = pd.DataFrame({'x (m)': np.around(coords, decimals=2),
                      'temperature (K)': temp_aa['temp'],
                      'change in fiss dens (1/m3s)': fiss_aa})
bb_df = pd.DataFrame({'y (m)': np.around(coords, decimals=2),
                      'temperature (K)': temp_bb['temp'],
                      'change in fiss dens (1/m3s)': fiss_bb})
aa_df.to_csv('moltres_1.2_AA', index=False, sep='\t')
bb_df.to_csv('moltres_1.2_BB', index=False, sep='\t')

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.interpolate as spi
sys.path.append(
        os.path.dirname(
                os.path.dirname(
                        os.path.abspath(__file__))))
from common_func import get_disc, get_benchmark_disc    # noqa: E402

# Data
pre_elemental = pd.read_csv('circ-fuel_csv_pre_elemental_0002.csv')
benchmark_aa = pd.read_csv('DNP_AA', delim_whitespace=True, header=None)
benchmark_bb = pd.read_csv('DNP_BB', delim_whitespace=True, header=None)

# Decay constant, lambda
lam = [0.0124667, 0.0282917, 0.0425244, 0.133042,
       0.292467, 0.666488, 1.63478, 3.5546]

# Pre-multiply with appropriate decay constant and sum at each position
pre_combined = np.zeros((200, 200))
for i in range(8):
    pre_id = 'pre' + str(i+1)
    pre_combined += np.reshape(np.array(pre_elemental[pre_id])
                               * lam[i] * 1e6 * 7.53085e17,
                               (200, 200))

# Interpolate from half centimeter to integer centimeter positions
x = np.linspace(0, 2, 201)
x_ext = np.linspace(.005, 1.995, 200)
pre_func = spi.interp2d(x_ext, x_ext, pre_combined, kind='linear')

# Extrapolate endpoints linearly from nearest two neighbors
pre_aa = pre_func(x, 1)
pre_bb = pre_func(1, x)
pre_aa[0] = pre_func(0.005, 1) - (pre_func(0.015, 1) - pre_func(0.005, 1)) / 2
pre_aa[-1] = pre_func(1.995, 1) + (pre_func(1.995, 1) - pre_func(1.985, 1)) / 2
pre_bb[0] = pre_func(1, 0.005) - (pre_func(1, 0.015) - pre_func(1, 0.005)) / 2
pre_bb[-1] = pre_func(1, 1.995) + (pre_func(1, 1.995) - pre_func(1, 1.985)) / 2

# Calculate % discrepancy
disc_aa_pre = get_disc(pre_aa, benchmark_aa)
disc_bb_pre = get_disc(pre_bb, benchmark_bb)

ave_aa, std_aa = get_benchmark_disc(benchmark_aa)
ave_bb, std_bb = get_benchmark_disc(benchmark_bb)

f = open('circ-fuel.txt', 'w')
f.write("Discrepancy in delayed neutron source along AA' = " +
        str(disc_aa_pre*100) + " %\n")
f.write("Discrepancy in delayed neutron source along BB' = " +
        str(disc_bb_pre[0]*100) + " %\n")
f.write("Benchmark average discrepancy in delayed neutron source along AA' = "
        + str(ave_aa*100) + " %\n")
f.write("Benchmark average discrepancy in delayed neutron source along BB' = "
        + str(ave_bb*100) + " %\n")
f.write("Benchmark discrepancy std dev in delayed neutron source along AA' = "
        + str(std_aa*100) + " %\n")
f.write("Benchmark discrepancy std dev in delayed neutron source along BB' = "
        + str(std_bb*100) + " %\n")
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
ax.plot(pre_bb, y, label='Moltres', color='tab:blue')
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
ax.set_xlim(0, 2.5e17)
ax.set_ylim(0, 2)
ax.set_ylabel(r'$y$ [m]')
ax.set_xlabel(r'Delayed neutron source [m$^{-3}\cdot$s$^{-1}$]')
plt.savefig('1-1-dnp-y-plot.png', dpi=400)

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
ax.plot(x, pre_aa, label='Moltres', color='tab:blue')
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
ax.set_ylim(0, 2.5e17)
ax.set_xlim(0, 2)
ax.set_xlabel(r'$x$ [m]')
ax.set_ylabel(r'Delayed neutron source [m$^{-3}\cdot$s$^{-1}$]')
plt.savefig('1-1-dnp-x-plot.png', dpi=400)

# %% Write tsv

coords = np.linspace(0, 2, 201)
aa_df = pd.DataFrame({'x (m)': np.around(coords, decimals=2),
                      'delayed n source (1/m3s)': pre_aa})
bb_df = pd.DataFrame({'y (m)': np.around(coords, decimals=2),
                      'delayed n source (1/m3s)': np.reshape(pre_bb, 201)})
aa_df.to_csv('moltres_1.1_AA', index=False, sep='\t')
bb_df.to_csv('moltres_1.1_BB', index=False, sep='\t')

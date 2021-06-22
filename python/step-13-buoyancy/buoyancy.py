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
from common_func import get_disc, get_benchmark_ave_disc

# Data
pre_elemental = pd.read_csv('buoyancy_out_ntsApp0_csv_pre_elemental_0054.csv')
temp_aa = pd.read_csv('buoyancy_csv_temp_aa_0028.csv')
temp_bb = pd.read_csv('buoyancy_csv_temp_bb_0028.csv')
vel_aa = pd.read_csv('buoyancy_csv_vel_aa_0028.csv')
vel_bb = pd.read_csv('buoyancy_csv_vel_bb_0028.csv')
data = pd.read_csv('../step-02-neutronics/nts_csv_aa_0002.csv')

benchmark_aa_pre = pd.read_csv('DNP_AA', delim_whitespace=True, header=None)
benchmark_bb_pre = pd.read_csv('DNP_BB', delim_whitespace=True, header=None)
benchmark_aa_temp = pd.read_csv('T_AA', delim_whitespace=True, header=None)
benchmark_bb_temp = pd.read_csv('T_BB', delim_whitespace=True, header=None)
benchmark_aa_ux = pd.read_csv('ux_AA', delim_whitespace=True, header=None)
benchmark_aa_uy = pd.read_csv('uy_AA', delim_whitespace=True, header=None)
benchmark_bb_uy = pd.read_csv('uy_BB', delim_whitespace=True, header=None)

# %% Precursor

# Decay constant, lambda
lam = [0.0124667, 0.0282917, 0.0425244, 0.133042,
       0.292467, 0.666488, 1.63478, 3.5546]

# Pre-multiply with appropriate decay constant and sum at each position
pre_combined = np.zeros((200, 200))
for i in range(8):
    pre_id = 'pre' + str(i+1)
    pre_combined += np.reshape(np.array(pre_elemental[pre_id])
                               * lam[i] * 1e6 * 7.6178e17,
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
disc_aa_pre = get_disc(pre_aa, benchmark_aa_pre)
disc_bb_pre = get_disc(pre_bb, benchmark_bb_pre)

x = np.arange(0, 201, 25)
aa_pre = np.zeros(len(x))
bb_pre = np.zeros(len(x))

for i in range(len(x)):
    aa_pre[i] = pre_aa[x[i]]
    bb_pre[i] = pre_bb[x[i]]

# %% Temperature

# Calculate % discrepancy
disc_aa_temp = get_disc(temp_aa['temp'], benchmark_aa_temp)
disc_bb_temp = get_disc(temp_bb['temp'], benchmark_bb_temp)

x = np.arange(0, 201, 25)
aa_temp = np.zeros(len(x))
bb_temp = np.zeros(len(x))

for i in range(len(x)):
    aa_temp[i] = temp_aa['temp'][x[i]]
    bb_temp[i] = temp_bb['temp'][x[i]]

# %% Velocity

# Calculate % discrepancy
disc_aa_ux = get_disc(vel_aa['vel_x'] / 100, benchmark_aa_ux)
disc_aa_uy = get_disc(vel_aa['vel_y'] / 100, benchmark_aa_uy)
disc_bb_uy = get_disc(vel_bb['vel_y'] / 100, benchmark_bb_uy)

x = np.arange(0, 201, 25)
aa_ux = np.zeros(len(x))
aa_uy = np.zeros(len(x))
bb_ux = np.zeros(len(x))
bb_uy = np.zeros(len(x))

for i in range(len(x)):
    aa_ux[i] = vel_aa['vel_x'][x[i]]
    aa_uy[i] = vel_aa['vel_y'][x[i]]
    bb_ux[i] = vel_bb['vel_x'][x[i]]
    bb_uy[i] = vel_bb['vel_y'][x[i]]

# %% Benchmark discrepancy

ave_aa_pre = get_benchmark_ave_disc(benchmark_aa_pre)
ave_bb_pre = get_benchmark_ave_disc(benchmark_bb_pre)
ave_aa_temp = get_benchmark_ave_disc(benchmark_aa_temp)
ave_bb_temp = get_benchmark_ave_disc(benchmark_bb_temp)
ave_aa_ux = get_benchmark_ave_disc(benchmark_aa_ux)
ave_aa_uy = get_benchmark_ave_disc(benchmark_aa_uy)
ave_bb_uy = get_benchmark_ave_disc(benchmark_bb_uy)

f = open('buoyancy.txt', 'w')
f.write("Discrepancy in delayed neutron source along AA' = " +
        str(disc_aa_pre*100) + " %\n")
f.write("Discrepancy in delayed neutron source along BB' = " +
        str(disc_bb_pre[0]*100) + " %\n")
f.write("Discrepancy in temperature along AA' = " +
        str(disc_aa_temp*100) + " %\n")
f.write("Discrepancy in temperature along BB' = " +
        str(disc_bb_temp*100) + " %\n")
f.write("Discrepancy in ux along AA' = " + str(disc_aa_ux*100) + " %\n")
f.write("Discrepancy in uy along AA' = " + str(disc_aa_uy*100) + " %\n")
f.write("Discrepancy in uy along BB' = " + str(disc_bb_uy*100) + " %\n")
f.write("Benchmark average discrepancy in delayed neutron source along AA' = "
        + str(ave_aa_pre*100) + " %\n")
f.write("Benchmark average discrepancy in delayed neutron source along BB' = "
        + str(ave_bb_pre*100) + " %\n")
f.write("Benchmark average discrepancy in temperature along AA' = " +
        str(ave_aa_temp*100) + " %\n")
f.write("Benchmark average discrepancy in temperature along BB' = " +
        str(ave_bb_temp*100) + " %\n")
f.write("Benchmark average discrepancy in ux along AA' = " +
        str(ave_aa_ux*100) + " %\n")
f.write("Benchmark average discrepancy in uy along AA' = " +
        str(ave_aa_uy*100) + " %\n")
f.write("Benchmark average discrepancy in uy along BB' = " +
        str(ave_bb_uy*100) + " %\n")
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
ax.plot(x, pre_aa, label='Moltres', color='tab:blue')
ax.plot(x, benchmark_aa_pre[:][2], label='CNRS-SP$_3$', color='tab:orange',
        linestyle='--')
ax.plot(x, benchmark_aa_pre[:][3], label='Polimi', color='tab:green',
        linestyle=':')
ax.plot(x, benchmark_aa_pre[:][4], label='PSI', color='tab:red',
        linestyle='-.')
ax.plot(x, benchmark_aa_pre[:][6], label='TUD-S$_6$', color='tab:cyan',
        linestyle=(0, (3, 1, 1, 1, 1, 1)))
ax.legend()
ax.grid(which='both')
ax.set_xlim(0, 2)
ax.set_ylim(0, 2.5e17)
ax.set_xlabel(r'$x$ [m]')
ax.set_ylabel(r'Delayed neutron source [m$^{-3}\cdot$s$^{-1}$]')
plt.savefig('1-3-dnp-plot.png', dpi=400)

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
ax.set_ylim(900, 1300)
ax.set_xlabel(r'$x$ [m]')
ax.set_ylabel(r'$T$ [K]')
plt.savefig('1-3-temp-plot.png', dpi=400)

fig, ax = plt.subplots(figsize=[6, 5])
ax.plot(x, vel_aa['vel_y'] / 100, label='Moltres', color='tab:blue')
ax.plot(x, benchmark_aa_uy[:][2], label='CNRS-SP$_3$', color='tab:orange',
        linestyle='--')
ax.plot(x, benchmark_aa_uy[:][3], label='Polimi', color='tab:green',
        linestyle=':')
ax.plot(x, benchmark_aa_uy[:][4], label='PSI', color='tab:red',
        linestyle='-.')
ax.plot(x, benchmark_aa_uy[:][6], label='TUD-S$_6$', color='tab:cyan',
        linestyle=(0, (3, 1, 1, 1, 1, 1)))
ax.legend()
ax.grid(which='both')
ax.set_xlim(0, 2)
ax.set_ylim(-.25, .2)
ax.set_xlabel(r'$x$ [m]')
ax.set_ylabel(r'$u_y$ [m$\cdot$s$^{-1}$]')
plt.tight_layout()
plt.savefig('1-3-vel-plot.png', dpi=400)

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
sys.path.append(
        os.path.dirname(
                os.path.dirname(
                        os.path.abspath(__file__))))
from common_func import get_disc

# Data
benchmark_phase = pd.read_csv('phase_shift',
                              delim_whitespace=True,
                              header=None)
benchmark_gain = pd.read_csv('gain',
                             delim_whitespace=True,
                             header=None)

# %% Phase shift and gain

# Calculate phase and gain from Moltres data
freq = np.array([.0125, .025, .05, .1, .2, .4, .8])
phase = np.zeros(len(freq))
gain = np.zeros(len(freq))

for i in range(1, len(freq)+1):
    tau = 1. / freq[i-1]
    df = pd.read_csv('transient-perturb-' + str(i) + '_csv.csv')
    coords, peaks = signal.find_peaks(df['powernorm'], height=1e7)
    phase[i-1] = -(df['time'][coords[-1]] % tau - tau / 4) * 360 * freq[i-1]

    coords, troughs = signal.find_peaks(-df['powernorm'], height=-1e7)
    p_ave = sum(df['powernorm'][-400:]) / 400
    gain[i-1] = (peaks['peak_heights'][-1] - p_ave) / p_ave / .1

# Calculate % discrepancy
disc_phase = get_disc(phase[::-1], benchmark_phase)
disc_gain = get_disc(gain[::-1], benchmark_gain)

ave_phase = 0
ave_gain = 0
for i in range(6):
    ave_phase += get_disc(benchmark_phase[:][i+1], benchmark_phase)
    ave_gain += get_disc(benchmark_gain[:][i+1], benchmark_gain)
ave_phase /= 6
ave_gain /= 6

f = open('phase_gain.txt', 'w')
f.write("Discrepancy in phase shift = " +
        str(disc_phase*100) + " %\n")
f.write("Discrepancy in gain = " +
        str(disc_gain*100) + " %\n")
f.write("Benchmark average discrepancy in phase shift = " +
        str(ave_phase*100) + " %\n")
f.write("Benchmark average discrepancy in gain = " +
        str(ave_gain*100) + " %\n")
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
ax.plot(freq, gain,
        label='Moltres',
        color='tab:blue',
        marker='o',
        markersize=6)
ax.plot(freq, benchmark_gain[:][2][::-1],
        label='CNRS-SP$_3$',
        color='tab:orange',
        linestyle='--',
        marker='s',
        fillstyle='none',
        markersize=6)
ax.plot(freq, benchmark_gain[:][3][::-1],
        label='Polimi',
        color='tab:green',
        linestyle=':',
        marker='$*$',
        fillstyle='none',
        markersize=6)
ax.plot(freq, benchmark_gain[:][4][::-1],
        label='PSI',
        color='tab:red',
        linestyle='-.',
        marker='v',
        fillstyle='none',
        markersize=6)
ax.plot(freq, benchmark_gain[:][6][::-1],
        label='TUD-S$_6$',
        color='tab:cyan',
        linestyle=(0, (3, 1, 1, 1, 1, 1)),
        marker='o',
        fillstyle='none',
        markersize=6)
ax.legend()
ax.set_yscale('log')
ax.set_xscale('log')
ax.grid(which='both')
ax.set_xlim(1e-2, 1)
ax.set_ylim(1e-2, 1)
ax.set_xlabel(r'$f$ [Hz]')
ax.set_ylabel(r'Gain [-]')
plt.savefig('2-1-gain-plot.png', dpi=400)

fig, ax = plt.subplots(figsize=[6, 5])
ax.plot(freq, phase,
        label='Moltres',
        color='tab:blue',
        marker='o',
        markersize=6)
ax.plot(freq, benchmark_phase[:][2][::-1],
        label='CNRS-SP$_3$',
        color='tab:orange',
        linestyle='--',
        marker='s',
        fillstyle='none',
        markersize=6)
ax.plot(freq, benchmark_phase[:][3][::-1],
        label='Polimi',
        color='tab:green',
        linestyle=':',
        marker='$*$',
        fillstyle='none',
        markersize=6)
ax.plot(freq, benchmark_phase[:][4][::-1],
        label='PSI',
        color='tab:red',
        linestyle='-.',
        marker='v',
        fillstyle='none',
        markersize=6)
ax.plot(freq, benchmark_phase[:][6][::-1],
        label='TUD-S$_6$',
        color='tab:cyan',
        linestyle=(0, (3, 1, 1, 1, 1, 1)),
        marker='o',
        fillstyle='none',
        markersize=6)
ax.legend()
ax.set_xscale('log')
ax.grid(which='both')
ax.set_xlim(1e-2, 1)
ax.set_ylim(-100, 0)
ax.set_xlabel(r'$f$ [Hz]')
ax.set_ylabel(r'Phase shift [$^\circ$]')
plt.savefig('2-1-phase-plot.png', dpi=400)

# %% Write tsv

df = pd.DataFrame({'f (Hz)': np.around(freq, decimals=4),
                   'gain': gain,
                   'phase_shift [deg]': np.around(phase, decimals=2)})
df.to_csv('moltres_2.1_gain_phaseshift', index=False, sep='\t')

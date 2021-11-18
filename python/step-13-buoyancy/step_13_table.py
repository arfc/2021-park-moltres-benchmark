import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Data
moltres = {}
moltres['aa'] = pd.read_csv('moltres_1.3_AA', sep='\t')
moltres['bb'] = pd.read_csv('moltres_1.3_BB', sep='\t')
data = pd.read_csv('../step-02-neutronics/nts_csv_aa_0002.csv')

benchmark = {}
benchmark['aa_pre'] = pd.read_csv('DNP_AA', delim_whitespace=True, header=None)
benchmark['bb_pre'] = pd.read_csv('DNP_BB', delim_whitespace=True, header=None)
benchmark['aa_temp'] = pd.read_csv('T_AA', delim_whitespace=True, header=None)
benchmark['bb_temp'] = pd.read_csv('T_BB', delim_whitespace=True, header=None)
benchmark['aa_ux'] = pd.read_csv('ux_AA', delim_whitespace=True, header=None)
benchmark['aa_uy'] = pd.read_csv('uy_AA', delim_whitespace=True, header=None)
benchmark['bb_uy'] = pd.read_csv('uy_BB', delim_whitespace=True, header=None)

codes = ['Moltres', 'CNRS-SP1', 'CNRS-SP3', 'PoliMi',
         'PSI', 'TUD-S2', 'TUD-S6']
x = np.arange(0, 201, 25)

var = {}
var['aa'] = ['ux', 'uy', 'temp', 'pre']
var['bb'] = ['uy', 'temp', 'pre']
cl = ['aa', 'bb']


def format_table_entry(data):
    data = map(
        lambda x: "{:.3e}".format(float(x)),
        data)
    data = list(
        map(
            lambda x: x.upper(),
            list(data)
            )
        )
    return data


data = {}
for i in range(len(cl)):
    for j in range(len(var[cl[i]])):
        for k in range(len(codes)):
            if codes[k] == 'Moltres':
                data[cl[i] + var[cl[i]][j] + ' ' + codes[k]] = \
                    format_table_entry(
                        moltres[cl[i]][moltres[cl[i]].keys()[j+1]][0:201:25])
            else:
                data[cl[i] + var[cl[i]][j] + ' ' + codes[k]] = \
                    format_table_entry(
                        benchmark[cl[i] + '_' + var[cl[i]][j]][0:201:25][k])

df = pd.DataFrame(data)
df.T.to_latex('step-13-table.tex')

# Python data analysis scripts

This directory contains python scripts and output data files from Moltres
in their respective subdirectories for the various steps of the benchmark.

To run the python scripts, use the following command:
```
python3 vel-field.py
```

Required python packages include:
- Numpy
- Pandas
- Matplotlib
- Scipy

The python scripts generate the plots used in the manuscript and txt files, which contain the average discrepancy
values for Moltres for the given observables. e.g. ```vel-field.py```
generates ```vel-field.txt``` which contains the average discrepancy values
for ux and uy along centerlines AA' and BB'.

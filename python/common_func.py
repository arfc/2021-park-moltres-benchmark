import numpy as np


def average_value(data):
    Nr, Nc = np.shape(data)
    values = np.zeros(Nr)
    for i in range(Nr):
        sum = 0
        for j in range(Nc-1):   # 1 column of x coordinate data
            sum += data[j+1][i]
        values[i] = sum / (Nc - 1)
    return values


def discrepancy(data, average):
    Nr = len(average)
    numerator, denominator = 0, 0
    for i in range(Nr):
        numerator += (data[i] - average[i])**2
        denominator += average[i]**2
    disc = np.sqrt(numerator / denominator)
    return disc


def get_disc(moltres_data, benchmark_data):
    ave = average_value(benchmark_data)
    disc = discrepancy(moltres_data, ave)
    return disc

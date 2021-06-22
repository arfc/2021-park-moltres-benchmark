import numpy as np


def average_value(data):
    """
    Calculates the pointwise average values for a given observable
    (e.g. temperature) using results from all CNRS benchmark software.

    Parameters
    ----------
    data : Pandas DataFrame
        Parsed pointwise data from a csv file containing observable data
        from all CNRS benchmark software.

    Returns
    -------
    values : Numpy array
        Pointwise average values of a given observable from the provided
        benchmark csv data.
    """
    Nr, Nc = np.shape(data)
    values = np.zeros(Nr)
    for i in range(Nr):
        sum = 0
        for j in range(Nc-1):   # first column consists x coordinates
            sum += data[j+1][i]
        values[i] = sum / (Nc - 1)
    return values


def discrepancy(data, average):
    """
    Calculates the average discrepancy of a given software's results against
    the benchmark pointwise average data according to the equation given by
    Tiberga et al. (2020).

    [1] Tiberga et al., "Results from a multi-physics numerical benchmark for
    codes dedicated to molten salt fast reactors", Annals of Nuclear Energy,
    vol. 142, July 2020, 107428.

    Parameters
    ----------
    data : Pandas DataFrame
        Parsed pointwise data from a csv file containing a given software's
        results for a given observable.
    average : Numpy array
        Pointwise average values of a given observable from the benchmark,
        generated beforehand using the average_value() function.

    Returns
    -------
    disc : float
        Average discrepancy of a given software's results for a given
        observable against the benchmark pointwise average data.
    """
    Nr = len(average)
    numerator, denominator = 0, 0
    for i in range(Nr):
        numerator += (data[i] - average[i])**2
        denominator += average[i]**2
    disc = np.sqrt(numerator / denominator)
    return disc


def get_disc(software_data, benchmark_data):
    """
    Calculates the average discrepancy of a given software's results
    against the benchmark pointwise average data. Uses average_value() to
    get the pointwise average values from the benchmark, before using
    discrepancy() to get the average discrepancy return parameter.

    Parameters
    ----------
    moltres_data : Pandas DataFrame
        Parsed pointwise data from a csv file containing Moltres' results for
        a given observable.
    benchmark_data : Pandas DataFrame
        Parsed pointwise data from a csv file containing observable data
        from all CNRS benchmark software.

    Returns
    -------
    disc : float
        Average discrepancy of Moltres' results for a given observable against
        the benchmark pointwise average data.
    """
    ave = average_value(benchmark_data)
    disc = discrepancy(software_data, ave)
    return disc


def get_benchmark_ave_disc(benchmark_data):
    """
    Calculates the overall benchmark average discrepancy against the benchmark
    pointwise average data. Uses average_value() to get the pointwise average
    values from the benchmark, before using discrepancy() to get the average
    discrepancy of each benchmark software. Finally, this function returns the
    average of all average discrepancies.

    Parameters
    ----------
    benchmark_data : Pandas DataFrame
        Parsed pointwise data from a csv file containing observable data
        from all CNRS benchmark software.

    Returns
    -------
    benchmark_ave_disc : float
        Average of all average discrepancy values from the benchmark software.
    """
    ave = average_value(benchmark_data)
    Nr, Nc = np.shape(benchmark_data)
    discs = np.zeros(Nc-1)
    for i in range(Nc-1):
        discs[i] = discrepancy(benchmark_data[i+1], ave)
    benchmark_ave_disc = np.average(discs)
    return benchmark_ave_disc

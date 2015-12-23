__author__ = 'rotem'


def trunc(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    return ('%.*f' % (n + 1, f))[:-1]


def is_out_of_upper_bound(measurement, mean, std):
    return measurement is not None and \
           (measurement > mean + std)


def is_out_of_lower_bound(measurement, mean, std):
    return measurement is not None and \
           (measurement < mean - std)


def is_out_of_bounds(measurement, mean, std):
    return is_out_of_upper_bound(measurement, mean, std) or \
           is_out_of_lower_bound(measurement, mean, std)


def get_mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/float(n)


def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = get_mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss


def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        return data[0]
        #raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5
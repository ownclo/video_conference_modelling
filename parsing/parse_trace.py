import sys
import re
import numpy

from scipy.stats import nbinom
import random

def neg_bin(mean, var):
    # Where does this is explained?
    p = mean / var
    n = mean * p / (1 - p)

    while(True):
        yield nbinom.rvs(n, p)

def dar(cor1, mean, var):
    neg_bin_seq = neg_bin(mean, var)
    prev = neg_bin_seq.next()

    while(True):
        if random.random() > cor1:
            prev = neg_bin_seq.next()
        yield prev

def take(n, seq):
    result = []
    for i in range(n):
        result.append(seq.next())
    return result

def get_sizes(tracefile):
    sizes = []
    for line in tracefile:
        for word in line.split():
            m = re.match(r"size=(\w+)$", word)
            if m:
                size = m.group(1)
                sizes.append(int(size))
    return sizes

def acf(x):
    """
    http://stackoverflow.com/q/14297012/190597
    http://en.wikipedia.org/wiki/Autocorrelation#Estimation
    """
    n = len(x)
    variance = x.var()
    wx = x-x.mean()
    r = numpy.correlate(wx, wx, mode = 'full')[-n:]
    result = r/variance/n
    return result


if __name__ == "__main__":
    tracefile = sys.argv[1]
    with open(tracefile) as f:
        sizes = numpy.array(get_sizes(f))

    mean = sizes.mean()
    var = sizes.var()

    corr = acf(sizes)
    cor1 = corr[1]

    print "N:", sizes.size
    print "Mean:", mean
    print "Variance:", var

    print "Autocorrelation (shift = 1):", cor1
    print "Autocorrelation (shift = 2):", corr[2]

    # Testing DAR distribution
    dar_seq = numpy.array(take(10000, dar(cor1, mean, var)))

    print dar_seq.mean(), dar_seq.var()
    print acf(dar_seq)[:3]

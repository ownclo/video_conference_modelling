import sys
import re
import numpy

from scipy.stats import nbinom
from scipy.stats import moment
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
        sizes = numpy.array(get_sizes(f)[1:])

    mean = sizes.mean()
    var = sizes.var()

    corr = acf(sizes)
    cor1 = corr[1]

    # # FRAME SIZES OVRER TIME
    # i = 1
    # for size in sizes:
    #     print i, size
    #     i += 1

    # # CORRELATION COEFFICIENTS OVER LAG (ACF)
    # for i in xrange(0, 100):
    #     print i, corr[i]

    # HISTOGRAM
    # hist, edges = numpy.histogram(sizes, density=True)

    # for e, h in zip(edges, hist):
    #     print e, h

    #print "N:", sizes.size
    #print "Mean:", mean
    #print "Variance:", var

    #print "Autocorrelation (shift = 1):", cor1
    #print "Autocorrelation (shift = 2):", corr[2]

    # Testing DAR distribution
    dar_seq = numpy.array(take(10000, dar(cor1, mean, var)))
    #hs, es = numpy.histogram(dar_seq, density=True)
    #for e, h in zip(es, hs):
        #print e, h

    #print "DAR(1) mean, var: ", dar_seq.mean(), dar_seq.var()
    dar_acf = acf(dar_seq)
    sizes_acf = acf(sizes)
    for i in xrange(0, 20):
        print i, sizes_acf[i], dar_acf[i]

    #print "\n"
    #for i in xrange(2, 7):
        #morig = moment(sizes, i)
        #mmodel = moment(dar_seq, i)

        #print morig, mmodel, morig/mmodel

import sys
import re
import numpy

from scipy.stats import nbinom
from scipy.stats import moment
import random

import pyeeg
import dar
import markovian_model_linear
import leaky_bucket as lb
import quantizers as qs

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

def histogram(seq):
    hs, es = numpy.histogram(seq, density=True)
    return zip(es, hs)

def model_summary(original, model):
    print "# FIRST SIX MOMENTS; ORIGINAL-MODEL"
    omean = original.mean()
    mmean = model.mean()
    print omean, mmean
    for i in xrange(2, 7):
        morig = moment(original, i)
        mmodel = moment(model, i)
        print morig, mmodel
    print "\n"

    print "# HISTOGRAM ORIGINAL"
    for e, h in histogram(original):
        print e, h
    print "\n"
    print "# HISTOGRAM MODEL"
    for e, h in histogram(model):
        print e, h
    print "\n"

    print "# AUTOCORRELATION FUNCTION ACF(LAG); ORIGINAL-MODEL"
    original_acf = acf(original)
    model_acf = acf(model)
    for i in xrange(0, 100):
        print i, original_acf[i], model_acf[i]
    print "\n"


if __name__ == "__main__":
    tracefile = sys.argv[1]
    with open(tracefile) as f:
        # NOTE: first frame must be skipped
        sizes = numpy.array(get_sizes(f)[1:])

    mean = sizes.mean()
    var = sizes.var()

    corr = acf(sizes)
    cor1 = corr[1]

    # # FRAME SIZES OVER TIME
    # i = 1
    # for size in sizes:
    #     print i, size
    #     i += 1

    # CORRELATION COEFFICIENTS OVER LAG (ACF)
    # for i in xrange(0, 5):
    #     print i, corr[i]
    # print pyeeg.hurst(sizes)

    drain_rate = sizes.mean()
    stdev = numpy.std(sizes)
    bucket_size = drain_rate + stdev

    # Testing DAR distribution
    dar_seq = numpy.array(take(10000, dar.dar1(cor1, mean, var)))
    # model_summary(sizes, dar_seq)

    # # Testing Markovian distribution
    num_quants = 20
    ml_seq = markovian_model_linear.gen_seq(sizes, 10000, num_quants, quantizer=qs.linear_quantizer)
    mk_seq = markovian_model_linear.gen_seq(sizes, 10000, num_quants, quantizer=qs.kmeans_quantizer)
    model_summary(sizes, ml_seq)
    model_summary(sizes, mk_seq)

    # for bs in numpy.arange(sizes.mean() - stdev, sizes.mean() + stdev, stdev / 10.0):
    #     num_loss = lb.leaky_bucket_loss(drain_rate, bs, sizes)
    #     dar_loss = lb.leaky_bucket_loss(drain_rate, bs, dar_seq)
    #     ml_loss = lb.leaky_bucket_loss(drain_rate, bs, ml_seq)
    #     print bs, num_loss * 1.0 / sum(sizes), dar_loss * 1.0 / numpy.sum(dar_seq), ml_loss * 1.0 / numpy.sum(ml_seq)

    # #dar_generator = dar.dar_p(sample_corrs, sample_mean, sample_var)
    # dar2_generator = dar.dar_p(corr[1:3], mean, var)

    # # Boris, Claire, MissAmerica - OK; Foreman, Suzie, Akiyo - NOP
    # # corrs = corr[1:3]
    # # p, alphas = dar.estimate_darp_probs(corrs)
    # # print alphas

    # dar2_seq = numpy.array(take(10000, dar2_generator))
    # model_summary(sizes, dar2_seq)

    # dar3_generator = dar.dar_p(corr[1:4], mean, var)
    # dar3_seq = numpy.array(take(10000, dar3_generator))
    # model_summary(sizes, dar3_seq)

    # dar4_generator = dar.dar_p(corr[1:5], mean, var)
    # dar4_seq = numpy.array(take(10000, dar4_generator))
    # model_summary(sizes, dar4_seq)

    # dar10_generator = dar.dar_p(corr[1:11], mean, var)
    # dar10_seq = numpy.array(take(10000, dar10_generator))
    # model_summary(sizes, dar10_seq)

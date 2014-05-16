from scipy.cluster.vq import kmeans
import numpy as np

def linear_quantizer(seq, num_quants):
    min_ = min(seq)
    max_ = max(seq)
    range_ = max_ - min_
    step = range_ * 1.0 / num_quants
    approx_dist = step / 2.0
    # print min_, max_, range_, step

    # Note: will not work if v not in [min, max]
    def quantize(v):
        i = 0
        t = min_
        tnext = t + step
        while(tnext < v):
            t = tnext
            tnext += step
        return int(round(t + approx_dist))

    return quantize

def kmeans_quantizer(seq, num_quants):
    aseq = np.array(seq)
    centroids, _ = kmeans(aseq, num_quants)

    def quantize(v):
        return nearest(v, centroids)

    return quantize


def nearest(point, seq):
    return min(seq, key = lambda x: abs(x - point))


if __name__ == "__main__":
    num_quants = 3
    seq = [10, 20, 30]
    quantize = linear_quantizer(seq, num_quants)

    qseq = map(quantize, seq)
    print qseq

    kquantize = kmeans_quantizer(seq, num_quants)
    print map(kquantize, seq)

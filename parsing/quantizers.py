
def linear_quantizer(seq, num_quants):
    min_ = min(seq)
    max_ = max(seq)
    range = max_ - min_
    step = range * 1.0 / num_quants
    approx_dist = step / 2.0

    def quantize(v):
        i = 0
        t = min_
        tnext = t + step
        while(tnext < v):
            t = tnext
            tnext += step
        return t + approx_dist

    return quantize

if __name__ == "__main__":
    num_quants = 2
    seq = [-1, -2, 0, 1, 2]
    quantize = linear_quantizer(seq, num_quants)

    qseq = map(quantize, seq)
    print qseq # [-1, -1, -1, 1, 1]

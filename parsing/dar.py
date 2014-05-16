import numpy as np
from scipy.stats import rv_discrete
from scipy.stats import nbinom
import random

def neg_bin(mean, var):
    # Where does this is explained?
    p = mean / var
    n = mean * p / (1 - p)

    while(True):
        yield nbinom.rvs(n, p)

def dar1(cor1, mean, var):
    neg_bin_seq = neg_bin(mean, var)
    prev = neg_bin_seq.next()

    while(True):
        if random.random() > cor1:
            prev = neg_bin_seq.next()
        yield prev

# will work for dar(2), won't for dar(3) and higher
def corrmatrix(corrs):
    init = np.insert(corrs[:-1], 0, 1)

    res = [init]
    for i in xrange(1, corrs.size):
        res.append(get_shifted_row(i, init))

    return np.array(res)

# XXX: does not work for ind == 0
def get_shifted_row(ind, row):
    rev_tail = row[1:][:ind][::-1]
    head = row[:-1*ind]
    return np.append(rev_tail, head)

def estimate_darp_probs(corrs):
    corrm = corrmatrix(corrs)
    xs = np.linalg.solve(corrm, corrs)

    p = sum(xs)
    alphas = [ x / p for x in xs ]
    return p, alphas

def push_sliding_window(window, item):
    del window[-1]
    window.insert(0, item)

def dar_p(corrs, mean, var):
    p, alphas = estimate_darp_probs(corrs)

    neg_bin_seq = neg_bin(mean, var)
    prev_window = [neg_bin_seq.next(), neg_bin_seq.next()]

    prev_dist = rv_discrete(name='prev_dist', values=(range(2), alphas))
    curr_dist = rv_discrete(name='curr_dist', values=([True, False], [p, 1.0 - p]))

    while(True):
        if curr_dist.rvs(): # take from history
            index = prev_dist.rvs()
            frame = prev_window[index]

            push_sliding_window(prev_window, frame)
            yield frame

        else: # generate new one
            frame = neg_bin_seq.next()
            push_sliding_window(prev_window, frame)
            yield frame


if __name__ == "__main__":
    cor1 = 0.89
    cor2 = 0.7999

    corrs = np.array([cor1, cor2])

    print estimate_darp_probs(corrs)
    print dar_p(corrs, 3287.0, 107880.85923).next()

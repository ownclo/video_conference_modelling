import numpy as np

def corrmatrix(corrs):
    init = np.insert(corrs[:-1], 0, 1)

    res = []
    for i in xrange(corrs.size):
        res.append(np.roll(init, i))

    return np.array(res)


if __name__ == "__main__":
    cor1 = 0.4
    cor2 = 0.3

    corrs = np.array([cor1, cor2])
    corrm = corrmatrix(corrs)

    xs = np.linalg.solve(corrm, corrs)

    print xs
    print np.allclose(np.dot(corrm,xs), corrs)

import numpy as np

def mean_rpis(Rpiss):
    n = len(Rpiss)
    m = len(Rpiss[0])

    begs = [0] * n
    ends = [0] * n
    for i in range(n):
        for j in range(m):
            begs[i] = Rpiss[i][j][0][0]
            ends[i] = Rpiss[i][j][0][-1]

    time = np.array([x / 60 for x in range(int(max(begs) * 6 + 1) * 10, int(min(ends)) * 60, 10)])

    l, = np.shape(time)

    res = np.zeros((n, m, l))

    for i in range(n):
        for j in range(m):
            t, Rpi = Rpiss[i][j]

            res[i, j, :] = Rpi[np.searchsorted(np.array(t), time)]

    res_mean = np.mean(res, axis=0)

    Rpis = []
    for j in range(m):
        Rpis.append((time, res_mean[j, :]))

    return Rpis


def mean_gpis(Gpiss):
    n = len(Gpiss)
    m = len(Gpiss[0])

    begs = [0] * n
    ends = [0] * n
    for i in range(n):
        for j in range(m):
            begs[i] = Gpiss[i][j][0][0]
            ends[i] = Gpiss[i][j][0][-1]

    time = np.array([x / 60 for x in range(int(max(begs) * 6 + 1) * 10, int(min(ends)) * 60, 10)])

    l, = np.shape(time)

    res = np.zeros((n, m, l))

    for i in range(n):
        for j in range(m):
            t, Gpi = Gpiss[i][j]

            res[i, j, :] = Gpi[np.searchsorted(np.array(t), time)]

    res_mean = np.mean(res, axis=0)

    Gpis = []
    for j in range(m):
        Gpis.append((time, res_mean[j, :]))

    return Gpis

#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from IPython import embed

from simulator import Simulator

if __name__ == "__main__":
    n = 100
    stats = []
    for i in range(n):
        stats.append(Simulator().run())
        print(i)

    total = {}
    for i in stats[0]:
        total[i] = np.array([x.get(i, 0) for x in stats])

    print(np.mean(total[2]))
    plt.hist(total[2], bins=20)
    plt.show()

    embed()

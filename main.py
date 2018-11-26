#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import json
from IPython import embed

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

from simulator import Simulator

if __name__ == "__main__":

    one = """
    n = 1000

    numsel = 2
    numhon = 2
    for spow in range(5, 95, 5):
        setup = [] # json.loads(open("setup.txt").read())
        for j in range(numsel):
            setup.append({'type': 'selfish', 'power': spow / numsel})
        for j in range(numhon):
            setup.append({'type': 'honest', 'power': (100 - spow) / numhon})
        print(setup)

        stats = []
        for i in range(n):
            stats.append(Simulator().run(setup))

        total = {}
        for i in range(7):
            total[i] = np.array([x.get(i, 0) for x in stats])

        print(np.mean(total[0]))
        print(np.mean(total[1]))


    # plt.hist(total[3], bins=20)
    # plt.show()
    #
    # embed()
    """

    two = """
    numsel = 2
    numhon = 2

    f0 = open("selfish0", 'w')
    f1 = open("selfish1", 'w')

    for spow in range(5, 95, 5):
        for sdif in range(40):
            setup = [] # json.loads(open("setup.txt").read())
            for j in range(numsel):
                setup.append({'type': 'selfish', 'power': spow / numsel * (1 - (2 * j - 1) * sdif / 100) })

            for j in range(numhon):
                setup.append({'type': 'honest', 'power': (100 - spow) / numhon})
            # print(setup)

            stats = []
            for i in range(n):
                stats.append(Simulator().run(setup))

            total = {}
            for i in range(7):
                total[i] = np.array([x.get(i, 0) for x in stats])

            print(np.mean(total[0]))
            print(np.mean(total[1]))

            f0.write("{}, ".format(np.mean(total[0])))
            f1.write("{}, ".format(np.mean(total[1])))

        f0.write("\n")
        f1.write("\n")
    """


    setup = json.loads(open("setup.txt").read())
    total_power = np.sum(np.array([float(x["power"]) for x in setup]))
    for i in setup:
        i["power"] /= total_power

    setup = sorted(setup, key=lambda x: x["type"])

    print(setup)

    stats = []

    head = Simulator().run(setup)
    time = head.time

    blocks = [0] * (head.height + 1)
    temp = head
    while temp is not None:
        blocks[temp.height] = temp
        temp = temp.prev

    colors = "bgrcmykw"


    c = {"honest": 0, "selfish": 0}
    for i in range(len(setup)):
        c[setup[i]["type"]] += 1
        base_x = [0, time / 3600]
        # base_y = [0, time / 600 * setup[si]["power"]]
        base_y = [0, time / 600 * setup[i]["power"]]
        plt.plot(base_x, base_y, "{}:".format(colors[i % 6]))
        selfish_x = [b.time / 3600 for b in blocks[1:]]
        selfish_y = np.cumsum(np.equal([b.miner.id_ for b in blocks[1:]], [i] * head.height))
        # selfish_y = np.cumsum([1] * head.height)
        label1 = "[{:.3f}] {}".format(setup[i]["power"], setup[i]["type"])
        label2 = r'${0}_{1}~({2}_{1} = {3:.2f})$'.format("S" if setup[i]["type"] == "selfish" else "H", c[setup[i]["type"]], "\\beta" if setup[i]["type"] == "selfish" else "\\alpha", setup[i]["power"])
        plt.plot(selfish_x, selfish_y, "{}".format(colors[i]), label=label2)

    base_t_x = [0, time / 3600]
    base_t_y = [0, time / 600]

    total_x = [b.time / 3600 for b in blocks[1:]]
    total_y = np.cumsum(np.ones(len(total_x)))

    plt.plot(base_t_x, base_t_y, "k:")
    plt.plot(total_x, total_y, "k", label="Total")

    plt.legend()
    plt.show()

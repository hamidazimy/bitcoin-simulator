#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import json
from IPython import embed

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
    #"""

    two = """
    n = 1
    numsel = 2
    numhon = 2

    f0 = open("selfish0_", 'w')
    f1 = open("selfish1_", 'w')

    for spow in range(5, 95, 5):
        for sdif in range(40):
            setup = [] # json.loads(open("setup.txt").read())
            for j in range(numsel):
                setup.append({'type': 'selfish', 'power': spow / numsel * (1 - (2 * j - 1) * sdif / 100)})

            for j in range(numhon):
                setup.append({'type': 'honest', 'power': (100 - spow) / numhon})
            # print(setup)

            stats = []
            for i in range(n):
                head = Simulator().run(setup)
                stat = {}
                for j in range(numhon + numsel):
                    stat[j] = 0

                temp = head
                while temp.height != 0:
                    stat[temp.miner.id_] = stat[temp.miner.id_] + 1
                    temp = temp.prev

                stats.append(stat)

            total = {}
            for i in range(7):
                total[i] = np.array([x.get(i, 0) for x in stats])

            print(np.mean(total[0]))
            print(np.mean(total[1]))

            f0.write("{}, ".format(np.mean(total[0])))
            f1.write("{}, ".format(np.mean(total[1])))

        f0.write("\n")
        f1.write("\n")
    #"""

    #three = """
    setup = json.loads(open("setup.txt").read())
    total_power = np.sum(np.array([float(x["power"]) for x in setup]))
    for i in setup:
        i["power"] /= total_power

    print(setup)

    stats = []

    head = Simulator().run(setup)
    time = head.time

    blocks = [0] * (head.height + 1)
    temp = head
    while temp is not None:
        blocks[temp.height] = temp
        temp = temp.prev

    colors = "rgbcmykw"

    for i in range(len(setup)):
        end_time = int(time / 3600)
        base_x = list(range(0, end_time, end_time // 10))
        end_revenue = int(time / 600 * setup[i]["power"])
        # base_y = [0, time / 600 * setup[si]["power"]]
        base_y = list(range(0, end_revenue, end_revenue // 10))
        if len(base_y) < len(base_x):
            base_y.append(base_y[1] + base_y[-1])
        if len(base_x) < len(base_y):
            base_x.append(base_x[1] + base_x[-1])
        print(base_y)
        plt.plot(base_x, base_y, "{}:*".format(colors[i]))
        selfish_x = [b.time / 3600 for b in blocks[1:]]
        selfish_y = np.cumsum(np.equal([b.miner.id_ for b in blocks[1:]], [i] * head.height))
        # selfish_y = np.cumsum([1] * head.height)
        # plt.plot(selfish_x, selfish_y, "{}".format(colors[i]), label="[{:.3f}] {}".format(setup[i]["power"], setup[i]["type"]))
        plt.plot(selfish_x, selfish_y, "{}".format(colors[i]), label="α = %{:2d} ({})".format(int(setup[i]["power"] * 100), setup[i]["type"]))

    # base_t_x = [0, time / 3600]
    # base_t_y = [0, time / 600]
    #
    # total_x = [b.time / 3600 for b in blocks[1:]]
    # total_y = np.cumsum(np.ones(len(total_x)))
    #
    # plt.plot(base_t_x, base_t_y, "k:")
    # plt.plot(total_x, total_y, "k", label="Total")

    plt.xlabel("Time in hours")
    plt.ylabel("Number of blocks generated")
    plt.legend()
    plt.show()
    #"""

#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import json
import math
from time import sleep
from IPython import embed

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

from simulator import Simulator
from multiproc import myProc
import multiprocessing

if __name__ == "__main__":
    colors = "rgbymckw"

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

    three = """
    setup = json.loads(open("setup.txt").read())
    total_power = np.sum(np.array([float(x["power"]) for x in setup]))
    for i in setup:
        i["power"] /= total_power

    setup = sorted(setup, key=lambda x: x["type"], reverse=True)
    print(setup)

    sim = Simulator(setup)
    sim.run()
    sim.analyze()

    colors = "rgbymckw"

    for i in range(len(setup)):
        t, Gpi = sim.Gpis[i]
        label = r"${0}_{1}~(\alpha_{1} = {2:.2f})$".format("S" if setup[i]["type"] == "selfish" else "H", i, setup[i]["power"])
        plt.ylim((-15, +15))
        plt.plot(t, Gpi, "{}".format(colors[i]), label=label)

    plt.plot([0, max(t)], [0, 0], "k--")

    plt.xlabel(r"$t$")
    plt.ylabel(r"$G_{P_i}(t)$")
    plt.legend()
    plt.show()
    #"""

    #eight = """
    setup = json.loads(open("setup.txt").read())
    total_power = np.sum(np.array([float(x["power"]) for x in setup]))
    for i in setup:
        i["power"] /= total_power

    setup = sorted(setup, key=lambda x: x["type"], reverse=True)

    number_of_procs = 3
    number_of_sims = 3

    simq = multiprocessing.JoinableQueue()
    resq = multiprocessing.Queue()
    procs = [myProc(simq, resq) for i in range(number_of_procs)]
    for p in procs:
        p.start()

    for c in range(number_of_sims):
        simq.put(Simulator(setup))
    for c in range(number_of_procs):
        simq.put(None)

    simq.join()

    while number_of_sims:
        result = resq.get()
        print(result)
        number_of_sims -= 1

    # time = np.array(range(10, 40320, 10))

    # results = []
    # while not q.empty():
    #     foo = q.get()
    #     print(foo)
    #     results.append(foo)

    # print(results)
    #
    # # for t_ in time[0:2]:
    # #     print("time: {}".format(t_))
    # c = 0
    # for p in range(number_of_procs):
    #     print("p: {}".format(p))
    #     for i in range(1):
    #         print("i: {}".format(i))
    #         print(len(results))
    #         print(len(results[p]))
    #         print(len(results[p][i]))
    #
    #         t, Gpi = results[0][i]
    #         # foo = np.argmax(np.where(Gpi < t_, Gpi, 0))
    #         # print(foo)
    #         label = r"${0}_{1}~(\alpha_{1} = {2:.2f})$".format("S" if setup[i]["type"] == "selfish" else "H", i, setup[i]["power"])
    #         plt.ylim((-15, +15))
    #         plt.plot(t, Gpi, "{}".format(colors[c]), label=label)
    #         c += 1
    #
    # # for i in range(len(setup)):
    # #     t, Gpi = results[0][i]
    # #     label = r"${0}_{1}~(\alpha_{1} = {2:.2f})$".format("S" if setup[i]["type"] == "selfish" else "H", i, setup[i]["power"])
    # #     plt.ylim((-15, +15))
    # #     plt.plot(t, Gpi, "{}".format(colors[i]), label=label)
    #
    #
    # plt.plot([0, max(t)], [0, 0], "k--")
    #
    # plt.xlabel(r"$t$")
    # plt.ylabel(r"$G_{P_i}(t)$")
    # plt.legend()
    # plt.show()




    # for i in range(len(setup)):
    #     t, Gpi = sim2.Gpis[i]
    #     label = r"${0}_{1}~(\alpha_{1} = {2:.2f})$".format("S" if setup[i]["type"] == "selfish" else "H", i, setup[i]["power"])
    #     plt.ylim((-15, +15))
    #     plt.plot(t, Gpi, "{}".format(colors[i]), label=label)
    #
    # plt.plot([0, max(t)], [0, 0], "k--")
    #
    # plt.xlabel(r"$t$")
    # plt.ylabel(r"$G_{P_i}(t)$")
    # plt.legend()
    # plt.show()
    #"""

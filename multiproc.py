import multiprocessing
import random
import numpy
from simulator import Simulator

class myProc(multiprocessing.Process):

    def __init__(self, simq, resq):
        multiprocessing.Process.__init__(self)
        self.simq = simq
        self.resq = resq

    def run(self):
        id = self.name
        numpy.random.seed(int(random.random() * 1000))
        print("Starting " + id)
        while True:
            sim = self.simq.get()
            if sim is None:
                self.simq.task_done()
                break
            print("Simulator {} started".format(sim.id))
            sim.run()
            sim.analyze()
            print("Simulator {} finished".format(sim.id))
            self.resq.put(sim.Gpis)
            self.simq.task_done()
        print("Exiting " + id)
        exit(0)

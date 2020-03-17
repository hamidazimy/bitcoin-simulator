import multiprocessing
import random
import numpy
from simulator import Simulator
import sys

class SimProcessor(multiprocessing.Process):

    def __init__(self, simq, resq):
        multiprocessing.Process.__init__(self)
        self.simq = simq
        self.resq = resq

    def run(self):
        id = self.name
        numpy.random.seed(int(random.random() * 1000))
        SimProcessor.log(f"Starting {id}\n")
        while True:
            sim = self.simq.get()
            if sim is None:
                self.simq.task_done()
                break
            SimProcessor.log(f"Simulator {sim.id} started")
            # sim.run(constant_propagation_delay=0)
            sim.run()
            sim.analyze()
            SimProcessor.log(f"Simulator {sim.id} finished")
            self.resq.put(sim.Gpis)
            self.simq.task_done()
        SimProcessor.log(f"Exiting {id}")

    @classmethod
    def log(cls, line):
        if False:
            sys.stderr.write(line)

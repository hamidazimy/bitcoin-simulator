import multiprocessing
import sys
import random
import numpy


class SimProcessor(multiprocessing.Process):

    verbose = False

    @classmethod
    def log(cls, line):
        if SimProcessor.verbose:
            sys.stderr.write(line)

    def __init__(self, simq, resq):
        multiprocessing.Process.__init__(self)
        self.simq = simq
        self.resq = resq

    def run(self):
        numpy.random.seed(int(random.random() * 1000))
        SimProcessor.log(f"Starting {self.name}\n")
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
            self.resq.put(sim.result)
            self.simq.task_done()
        SimProcessor.log(f"Exiting {self.name}")

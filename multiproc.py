import multiprocessing
from simulator import Simulator

class myProc(multiprocessing.Process):

    def __init__(self, simq, resq):
        multiprocessing.Process.__init__(self)
        self.simq = simq
        self.resq = resq

    def run(self):
        id = self.name
        print ("Starting " + id)
        while True:
            sim = self.simq.get()
            if sim is None:
                print("Exiting " + id)
                self.simq.task_done()
                break
            print(sim)
            sim.run()
            sim.analyze()
            Gpis = sim.Gpis
            self.simq.task_done()
            self.resq.put(Gpis)

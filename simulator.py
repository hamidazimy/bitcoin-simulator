import numpy
import time
import json

from queue import PriorityQueue


class Simulator:
    """Simulator!"""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Simulator, cls).__new__(cls)
        return cls._instance

    def __init__(self, verbose=False):
        if hasattr(Simulator._instance, 'time'):
            return

        self.verbose = verbose
        self.time = 0
        self.q = PriorityQueue()
        self.miners = []
        Simulator._difficulty_coefficient = 1
        Simulator._last_difficulty_update_time = 0


    def run(self, setup, constant_propagation_delay=None):

        self.time = 0
        self.q = PriorityQueue()
        self.miners = []
        Simulator._difficulty_coefficient = 1
        Simulator._last_difficulty_update_time = 0

        genesis = Block()
        # setup = json.loads(open("setup.txt").read())
        total_power = numpy.sum(numpy.array([float(x["power"]) for x in setup]))
        id = 0
        for i in setup:
            if i["type"] == "honest":
                self.miners.append(Miner(id, i["power"] / total_power, genesis))
            if i["type"] == "selfish" or i["type"] == "bipolar":
                self.miners.append(Selfish(id, i["power"] / total_power, genesis, i["type"] == "bipolar"))
            id += 1


        q = self.q

        n = len(self.miners)

        found = [numpy.random.exponential(600 / m.power) for m in self.miners]
        for i in range(n):
            q.put(Event(found[i], EventType.NewBlockFound, self.miners[i], self.miners[i].head))

        if constant_propagation_delay is not None:
            Miner.constant_propagation_delay = constant_propagation_delay

        head = Block()
        while head.height < 40320:
            next_event = q.get()
            self.time = next_event.time
            consequences, new_head = next_event.occur()
            if new_head is not None and new_head.height > head.height:
                head = new_head
                if head.height % 2016 == 0:
                    prev_diffculty = Simulator._difficulty_coefficient
                    Simulator._difficulty_coefficient *= (2016 * 600) / (head.time - Simulator._last_difficulty_update_time)
                    Simulator().log("{}".format(head))
                    Simulator().log("Mean block generation time in the last period: {:6.2f}".format((head.time - Simulator._last_difficulty_update_time) / 2016))
                    Simulator().log("Difficulty adjustment: ({:.3f}) → ({:.3f})".format(prev_diffculty, Simulator._difficulty_coefficient))
                    Simulator._last_difficulty_update_time = head.time
            for c in consequences:
                q.put(c)
            # time.sleep(1)

        return head

    def log(self, text):
        if Simulator().verbose:
            print(text)


from event import Event, EventType
from block import Block
from miner import Miner, Selfish

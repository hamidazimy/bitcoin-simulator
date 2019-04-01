import numpy as np
import time
import json

from queue import PriorityQueue


class Simulator:
    """Simulator!"""

    def __init__(self, setup, verbose=False):
        self.verbose = verbose
        self.setup = setup
        self.time = 0
        self.q = PriorityQueue()
        self.miners = []
        self._difficulty_coefficient = 1
        self._last_difficulty_update_time = 0
        self.head = None


    def run(self, constant_propagation_delay=None):

        self.time = 0
        self.q = PriorityQueue()
        self.miners = []
        self._difficulty_coefficient = 1
        self._last_difficulty_update_time = 0

        genesis = Block()
        # setup = json.loads(open("setup.txt").read())
        total_power = np.sum(np.array([float(x["power"]) for x in self.setup]))
        id = 0
        for i in self.setup:
            if i["type"] == "honest":
                self.miners.append(Miner(id, i["power"] / total_power, genesis, self, constant_propagation_delay))
            if i["type"] == "selfish" or i["type"] == "bipolar":
                self.miners.append(Selfish(id, i["power"] / total_power, genesis, self, constant_propagation_delay, i["type"] == "bipolar"))
            id += 1


        q = self.q

        n = len(self.miners)

        found = [np.random.exponential(600 / m.power) for m in self.miners]
        for i in range(n):
            q.put(Event(found[i], EventType.NewBlockFound, self.miners[i], self.miners[i].head))

        head = Block()
        while head.height < 40320:
            next_event = q.get()
            self.time = next_event.time
            consequences, new_head = next_event.occur()
            if new_head is not None and new_head.height > head.height:
                head = new_head
                if head.height % 2016 == 0:
                    prev_diffculty = self._difficulty_coefficient
                    self._difficulty_coefficient *= (2016 * 600) / (head.time - self._last_difficulty_update_time)
                    self.log("{}".format(head))
                    self.log("Mean block generation time in the last period: {:6.2f}".format((head.time - self._last_difficulty_update_time) / 2016))
                    self.log("Difficulty adjustment: ({:.3f}) → ({:.3f})".format(prev_diffculty, self._difficulty_coefficient))
                    self._last_difficulty_update_time = head.time
            for c in consequences:
                q.put(c)
            # time.sleep(1)

        self.head = head
        return head

    def log(self, text):
        if self.verbose:
            print(text)


from event import Event, EventType
from block import Block
from miner import Miner, Selfish

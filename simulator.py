import numpy as np
import time
import json

from queue import PriorityQueue


class Simulator:
    """Simulator!"""
    instance_count = 0

    MAX_HEIGHT = 3000

    def __init__(self, setup, verbose=False):
        self.id = str(Simulator.instance_count)
        Simulator.instance_count += 1
        self.verbose = verbose
        self.setup = setup
        self.time = 0
        self.miners = []
        self._difficulty_coefficient = 1
        self._last_difficulty_update_time = 0
        self.head = None
        self.Rpis = []
        self.Gpis = []
        self.gamma = 0


    def run(self, constant_propagation_delay=None):

        self.time = 0
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
            if i["type"] == "selfish":
                self.miners.append(Selfish(id, i["power"] / total_power, genesis, self, constant_propagation_delay))
            if i["type"] == "semi":
                self.miners.append(SemiSelfish(id, i["power"] / total_power, genesis, self, constant_propagation_delay))
            id += 1


        q = PriorityQueue()

        n = len(self.miners)

        found = [np.random.exponential(600 / m.power) for m in self.miners]
        for i in range(n):
            q.put(Event(found[i], EventType.NewBlockFound, self.miners[i], self.miners[i].head))

        head = Block()
        while head.height < Simulator.MAX_HEIGHT:
            next_event = q.get()
            self.time = next_event.time
            consequences, new_head = next_event.occur()
            if new_head is not None and new_head.height > head.height:
                head = new_head
                if head.height % 2016 == 0:
                    if head.height == 2016:
                        print(f"{head.time:.1f}\t")
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

    def analyze(self):
        head = self.head

        blocks = [None] * (head.height + 1)
        temp = head
        while temp is not None:
            blocks[temp.height] = temp
            temp = temp.prev

        self.log("{}".format(blocks[-1]))

        gammas = []
        for i in range(len(self.setup)):
            t = np.array([b.time / 3600 for b in blocks[1:]])
            Rpi = np.cumsum(np.equal([b.miner.id_ for b in blocks[1:]], [i] * head.height))
            Gpi = (Rpi - self.setup[i]["power"] * (t * 6)) / (t * 6) * 100
            self.Rpis.append((t, Rpi))
            self.Gpis.append((t, Gpi))
            if self.setup[i]["type"] == "honest":
                gammas.append(self.miners[i].gamma())
        self.gamma = (0 if len(gammas) == 0 else (sum(gammas) / len(gammas)))


    def log(self, text):
        if self.verbose:
            print(text)


from event import Event, EventType
from block import Block
from miner import Miner, Selfish, SemiSelfish

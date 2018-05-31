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

    def __init__(self):
        if hasattr(Simulator._instance, 'time'):
            return

        self.time = 0
        self.q = PriorityQueue()
        self.miners = []


    def run(self, setup):

        self.time = 0
        self.q = PriorityQueue()
        self.miners = []

        genesis = Block()
        # setup = json.loads(open("setup.txt").read())
        total = numpy.sum(numpy.array([float(x["power"]) for x in setup]))
        id = 0
        for i in setup:
            if i["type"] == "honest":
                self.miners.append(Miner(id, i["power"] / total, genesis))
            if i["type"] == "selfish":
                self.miners.append(Selfish(id, i["power"] / total, genesis))
            id += 1


        q = self.q

        n = len(self.miners)

        found = [numpy.random.exponential(600 / m.power) for m in self.miners]
        for i in range(n):
            q.put(Event(found[i], EventType.NewBlockFound, self.miners[i], self.miners[i].head))

        head = Block()
        while head.height < 100:
            next_event = q.get()
            self.time = next_event.time
            consequences, new_head = next_event.occur()
            if new_head is not None and new_head.height > head.height:
                head = new_head
            for c in consequences:
                q.put(c)
            # time.sleep(1)

        temp = head
        # print("\n====[Blockchain]================")
        # while True:
        #     print("[#{} by M{} at {:.2f}]⤦".format(temp.height, temp.miner.id_, temp.time))
        #     temp = temp.prev
        #     if temp.prev is None:
        #         print("[#0 GENESIS BLOCK]")
        #         break

        return self.stats(head)

    def stats(self, head):
        stat = {}
        while head.prev is not None:
            stat[head.miner.id_] = (0 if head.miner.id_ not in stat.keys() else stat[head.miner.id_]) + 1
            head = head.prev

        # print(stat)
        return stat


    def log(self, text):
        # print(text)
        pass


from event import Event, EventType
from block import Block
from miner import Miner, Selfish

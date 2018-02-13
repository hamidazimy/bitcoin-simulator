import numpy

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

        genesis = Block()
        with open("setup.txt") as f:
            powers = numpy.array([float(x) for x in f.readline().strip().split()])

        powers /= numpy.sum(powers)

        self.miners = [Miner(i, powers[i], genesis) for i in range(len(powers))]

    def run(self):
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
            if new_head is not None:
                head = new_head
            for c in consequences:
                q.put(c)

        print("\n====[Blockchain]================")
        while True:
            print("[#{} by M{} at {:.2f}]⤦".format(head.height, head.miner.id_, head.time))
            head = head.prev
            if head.prev is None:
                print("[#0 GENESIS BLOCK]")
                break

    def log(self, text):
        print(text)


from event import Event, EventType
from block import Block
from miner import Miner

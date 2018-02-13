import numpy

from simulator import Simulator
from event import Event, EventType
from block import Block

from csi import CSI


class Miner:
    """Miner!"""

    def __init__(self, id_, power, head):
        self.id_ = id_
        self.power = power
        self.head = head

    def __str__(self):
        return "M{} ({})".format(self.id_, self.power)

    def perform(self, event):
        if event.type_ == EventType.NewBlockFound:
            if event.head == self.head:
                Simulator().log("{}{}{:^11.2f}{}".format(CSI.BG_MG, CSI.FG_BK, event.time, CSI.RESET))
                self.head = Block(self.head.height + 1, event.time, self, self.head)
                Simulator().log("Miner {} found new block! {}".format(self.id_, self.head))
                consequences = []
                consequences += [Event(event.time + self.generation_time(), EventType.NewBlockFound, self, self.head)]
                consequences += [Event(event.time + Miner.propagation_delay(), EventType.NewBlockReceived, m, self.head)
                                 for m in Simulator().miners if m != self]
                return consequences, self.head
            else:
                # Miner is no longer mining on top of this block.
                return [], None
        elif event.type_ == EventType.NewBlockReceived:
            Simulator().log("{}{}{:^11.2f}{}".format(CSI.BG_CY, CSI.FG_BK, event.time, CSI.RESET))
            Simulator().log("Miner {} received new block! {}".format(self.id_, event.head))
            if self.head.height < event.head.height:
                self.head = event.head
                return [Event(event.time + self.generation_time(), EventType.NewBlockFound, self, self.head)], None
            else:
                Simulator().log("Current Head is: {}".format(self.head))
                temp = self.head
                while temp.height != event.head.height:
                    temp = temp.prev
                if temp.miner.id_ == event.head.miner.id_:
                    Simulator().log("{}{} NEXT BLOCK IS RECEIVED EARLIER! {}".format(CSI.FG_YL, CSI.REVERSE, CSI.RESET))
                else:
                    Simulator().log("{}{} FORK!!! {}".format(CSI.FG_RD, CSI.REVERSE, CSI.RESET))
                    Simulator().log("Newly received block discarded.")
                return [], None

    def generation_time(self):
        return numpy.random.exponential(600 / self.power)

    @classmethod
    def propagation_delay(cls):
        return numpy.random.gamma(1.26, 10)

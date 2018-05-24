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
            if event.head != self.head:
                # Miner is no longer mining on top of this block.
                return [], None
            return self.generate(event)
        elif event.type_ == EventType.NewBlockReceived:
            return self.receive(event)

    def generate(self, event):
        Simulator().log("{}{}{:^11.2f}{}".format(CSI.BG_MG, CSI.FG_BK, event.time, CSI.RESET))
        self.head = Block(self.head.height + 1, event.time, self, self.head)
        Simulator().log("Miner {} found new block! {}".format(self.id_, self.head))
        consequences = []
        consequences += [Event(event.time + self.generation_time(), EventType.NewBlockFound, self, self.head)]
        consequences += [Event(event.time + Miner.propagation_delay(), EventType.NewBlockReceived, m, self.head)
                            for m in Simulator().miners if m != self]
        return consequences, self.head

    def receive(self, event):
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


class Selfish(Miner):
    """Selfish Miner!"""

    def __init__(self, id_, power, head):
        super().__init__(id_, power, head)
        self.public = head

    def generate(self, event):
        delta = self.head.height - self.public.height
        Simulator().log("{}{}{:^11.2f}{}".format(CSI.BG_MG, CSI.FG_BK, event.time, CSI.RESET))
        self.head = Block(self.head.height + 1, event.time, self, self.head)
        Simulator().log("Miner {} found new block! {}".format(self.id_, self.head))
        consequences = []
        consequences += [Event(event.time + self.generation_time(), EventType.NewBlockFound, self, self.head)]
        if delta == 0 and self.head.prev != self.public:
            consequences += [Event(event.time + Selfish.propagation_delay(), EventType.NewBlockReceived, m, self.head)
                             for m in Simulator().miners if m != self]
        return consequences, self.head

    def receive(self, event):
        delta = self.head.height - self.public.height
        Simulator().log("{}{}{:^11.2f}{}".format(CSI.BG_CY, CSI.FG_BK, event.time, CSI.RESET))
        Simulator().log("Miner {} received new block! {}".format(self.id_, event.head))
        if self.public.height < event.head.height:
            self.public = event.head
            if delta < 1:
                self.head = event.head
                return [Event(event.time + self.generation_time(), EventType.NewBlockFound, self, self.head)], None
            elif delta == 1 or delta == 2:
                Simulator().log("Publishing: {}".format(self.head))
                return [Event(event.time + Selfish.propagation_delay(), EventType.NewBlockReceived, m, self.head)
                                 for m in Simulator().miners if m != self], None
            else:
                publishable = self.head
                while publishable.height > event.head.height:
                    publishable = publishable.prev
                Simulator().log("Publishing: {}".format(publishable))
                return [Event(event.time + Selfish.propagation_delay(), EventType.NewBlockReceived, m, publishable)
                                 for m in Simulator().miners if m != self], None
        else:
            Simulator().log("Current Head is: {}".format(self.head))
            temp = self.public
            while temp.height != event.head.height:
                temp = temp.prev
            if temp.miner.id_ == event.head.miner.id_:
                Simulator().log("{}{} NEXT BLOCK IS RECEIVED EARLIER! {}".format(CSI.FG_YL, CSI.REVERSE, CSI.RESET))
            else:
                Simulator().log("{}{} FORK!!! {}".format(CSI.FG_RD, CSI.REVERSE, CSI.RESET))
                Simulator().log("Newly received block discarded.")
            return [], None

    @classmethod
    def propagation_delay(cls):
        return 0.1 #numpy.random.gamma(1.26, 10)
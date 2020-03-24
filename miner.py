import numpy

from simulator import Simulator
from event import Event, EventType
from block import Block

from csi import CSI


class Miner:
    """Miner!"""

    def __init__(self, id_, power, head, simulator, constant_propagation_delay=None):
        self.id_ = id_
        self.power = power
        self.head = head
        self.simulator = simulator
        self.constant_propagation_delay = constant_propagation_delay
        self.gamma_num = 0
        self.gamma_den = 0

    def __str__(self):
        return "M{} ({})".format(self.id_, self.power)

    def gamma(self):
        return (0 if self.gamma_den == 0 else (self.gamma_num / self.gamma_den))

    def perform(self, event):
        if event.type_ == EventType.NewBlockFound:
            if event.head != self.head:
                # Miner is no longer mining on top of this block.
                return [], None
            return self.generate(event)
        elif event.type_ == EventType.NewBlockReceived:
            return self.receive(event)

    def generate(self, event):
        self.simulator.log("{}{}{:^11.2f}{}".format(CSI.BG_MG, CSI.FG_BK, event.time, CSI.RESET))
        self.head = Block(self.head.height + 1, self.simulator.difficulty_coefficient, event.time, self, self.head)
        self.simulator.log("Miner {} found new block! {}".format(self.id_, self.head))
        consequences = []
        consequences += [Event(event.time + self.generation_time(), EventType.NewBlockFound, self, self.head)]
        consequences += [Event(event.time + self.propagation_delay(), EventType.NewBlockReceived, m, self.head)
                         for m in self.simulator.miners if m != self]
        return consequences, self.head

    def receive(self, event):
        self.simulator.log("{}{}{:^11.2f}{}".format(CSI.BG_CY, CSI.FG_BK, event.time, CSI.RESET))
        self.simulator.log("Miner {} received new block! {}".format(self.id_, event.head))
        if self.head.height < event.head.height:
            self.head = event.head
            return [Event(event.time + self.generation_time(), EventType.NewBlockFound, self, self.head)], None
        else:
            self.simulator.log("Current Head is: {}".format(self.head))
            temp = self.head
            while temp.height != event.head.height:
                temp = temp.prev
            if temp.miner.id_ == event.head.miner.id_:
                self.simulator.log("{}{} NEXT BLOCK IS RECEIVED EARLIER! {}".format(CSI.FG_YL, CSI.REVERSE, CSI.RESET))
            else:
                self.simulator.log("{}{} FORK!!! {}".format(CSI.FG_RD, CSI.REVERSE, CSI.RESET))
                self.simulator.log("Newly received block discarded.")
                self.gamma_den += 1
                if isinstance(temp.miner, Selfish) or isinstance(temp.miner, SemiSelfish):
                    self.gamma_num += 1
            return [], None

    def generation_time(self):
        return numpy.random.exponential(600 / self.power * self.simulator.difficulty_coefficient)

    def propagation_delay(self):
        if self.constant_propagation_delay is not None:
            return self.constant_propagation_delay
        return numpy.random.gamma(1.26, 10)


class Selfish(Miner):
    """Selfish Miner!"""

    def __init__(self, id_, power, head, simulator, constant_propagation_delay=None, delay=0):
        super().__init__(id_, power, head, simulator, constant_propagation_delay)
        self.public = head
        self.delay = delay

    def generate(self, event):
        if self.head.height < self.delay:
            return super().generate(event)
        delta = self.head.height - self.public.height
        self.simulator.log("{}{}{:^11.2f}{}".format(CSI.BG_MG, CSI.FG_BK, event.time, CSI.RESET))
        self.head = Block(self.head.height + 1, self.simulator.difficulty_coefficient, event.time, self, self.head)
        self.simulator.log("Miner {} found new block! {}".format(self.id_, self.head))
        consequences = []
        consequences += [Event(event.time + self.generation_time(), EventType.NewBlockFound, self, self.head)]
        if delta == 0 and self.head.prev != self.public:
            consequences += [Event(event.time + self.propagation_delay(), EventType.NewBlockReceived, m, self.head)
                             for m in self.simulator.miners if m != self]
        return consequences, self.head

    def receive(self, event):
        if self.head.height < self.delay:
            return super().receive(event)
        delta = self.head.height - self.public.height
        self.simulator.log("{}{}{:^11.2f}{}".format(CSI.BG_CY, CSI.FG_BK, event.time, CSI.RESET))
        self.simulator.log("Miner {} received new block! {}".format(self.id_, event.head))
        if self.public.height < event.head.height:
            self.public = event.head
            if delta < 1:
                self.head = event.head
                return [Event(event.time + self.generation_time(), EventType.NewBlockFound, self, self.head)], None
            elif delta == 1 or delta == 2:
                self.simulator.log("Publishing: {}".format(self.head))
                return [Event(event.time + self.propagation_delay(), EventType.NewBlockReceived, m, self.head)
                                 for m in self.simulator.miners if m != self], None
            else:
                publishable = self.head
                while publishable.height > event.head.height:
                    publishable = publishable.prev
                self.simulator.log("Publishing: {}".format(publishable))
                return [Event(event.time + self.propagation_delay(), EventType.NewBlockReceived, m, publishable)
                                 for m in self.simulator.miners if m != self], None
        else:
            self.simulator.log("Current Head is: {}".format(self.head))
            temp = self.public
            while temp.height != event.head.height:
                temp = temp.prev
            if temp.miner.id_ == event.head.miner.id_:
                self.simulator.log("{}{} NEXT BLOCK IS RECEIVED EARLIER! {}".format(CSI.FG_YL, CSI.REVERSE, CSI.RESET))
            else:
                self.simulator.log("{}{} FORK!!! {}".format(CSI.FG_RD, CSI.REVERSE, CSI.RESET))
                self.simulator.log("Newly received block discarded.")
            return [], None


class SemiSelfish(Selfish):
    """Semi-Selfish Miner!"""

    def __init__(self, id_, power, head, simulator, constant_propagation_delay=None, delay=0, degree=2):
        super().__init__(id_, power, head, simulator, constant_propagation_delay, delay)
        self.degree = degree

    def generate(self, event):
        if self.head.height < self.delay:
            return super().generate(event)
        delta = self.head.height - self.public.height
        self.simulator.log("{}{}{:^11.2f}{}".format(CSI.BG_MG, CSI.FG_BK, event.time, CSI.RESET))
        self.head = Block(self.head.height + 1, self.simulator.difficulty_coefficient, event.time, self, self.head)
        self.simulator.log("Miner {} found new block! {}".format(self.id_, self.head))
        consequences = []
        consequences += [Event(event.time + self.generation_time(), EventType.NewBlockFound, self, self.head)]
        if delta == 0 and self.head.prev != self.public:
            consequences += [Event(event.time + self.propagation_delay(), EventType.NewBlockReceived, m, self.head)
                             for m in self.simulator.miners if m != self]
        if delta == self.degree:
            publishable = self.head
            for i in range(self.degree):
                publishable = publishable.prev
            consequences += [Event(event.time + self.propagation_delay(), EventType.NewBlockReceived, m, publishable)
                             for m in self.simulator.miners if m != self]
        return consequences, self.head

    def receive(self, event):
        if self.head.height < self.delay:
            return super().receive(event)
        delta = self.head.height - self.public.height
        self.simulator.log("{}{}{:^11.2f}{}".format(CSI.BG_CY, CSI.FG_BK, event.time, CSI.RESET))
        self.simulator.log("Miner {} received new block! {}".format(self.id_, event.head))
        if self.public.height < event.head.height:
            self.public = event.head
            if delta < 1:
                self.head = event.head
                return [Event(event.time + self.generation_time(), EventType.NewBlockFound, self, self.head)], None
            elif delta == 1 or delta == 2:
                self.simulator.log("Publishing: {}".format(self.head))
                return [Event(event.time + self.propagation_delay(), EventType.NewBlockReceived, m, self.head)
                                 for m in self.simulator.miners if m != self], None
            else:
                publishable = self.head
                while publishable.height > event.head.height:
                    publishable = publishable.prev
                self.simulator.log("Publishing: {}".format(publishable))
                return [Event(event.time + self.propagation_delay(), EventType.NewBlockReceived, m, publishable)
                                 for m in self.simulator.miners if m != self], None
        else:
            self.simulator.log("Current Head is: {}".format(self.head))
            temp = self.public
            while temp.height != event.head.height:
                temp = temp.prev
            if temp.miner.id_ == event.head.miner.id_:
                self.simulator.log("{}{} NEXT BLOCK IS RECEIVED EARLIER! {}".format(CSI.FG_YL, CSI.REVERSE, CSI.RESET))
            else:
                self.simulator.log("{}{} FORK!!! {}".format(CSI.FG_RD, CSI.REVERSE, CSI.RESET))
                self.simulator.log("Newly received block discarded.")
            return [], None

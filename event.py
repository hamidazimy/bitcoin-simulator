from enum import Enum

from csi import CSI


class EventType(Enum):
    NotDefined = 0
    NewBlockFound = 1
    NewBlockReceived = 2


class Event:
    """Events!"""

    def __init__(self, time=0, type_=EventType.NotDefined, miner=None, head=None):
        self.time = time
        self.type_ = type_
        self.miner = miner
        self.head = head

    def __str__(self):
        return "{}{} by M{} [{:.2f}]{}"\
            .format(CSI.FG_GN,
                    "New block found" if self.type_ == EventType.NewBlockFound else "New block received",
                    self.miner.id_,
                    self.time,
                    CSI.RESET)

    def __lt__(self, other):
        return self.time < other.time

    def occur(self):
        return self.miner.perform(self)

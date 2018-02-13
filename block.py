class Block:
    """Block!"""

    def __init__(self, height=0, time=0, miner=None, prev=None):
        self.height = height
        self.time = time
        self.miner = miner
        self.prev = prev

    def __str__(self):
        ret = ""
        head = self
        for i in range(3):
            if head.prev is None:
                return ret + "[#0 GENESIS BLOCK]"
            ret += "[#{} by M{} at {:.2f}]⟶".format(head.height, head.miner.id_, head.time)
            head = head.prev
        return ret + "..."

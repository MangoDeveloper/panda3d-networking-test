from direct.distributed import DistributedSmoothNodeAI

class DistributedToonAI(DistributedSmoothNodeAI.DistributedSmoothNodeAI):
    def __init__(self, air):
        DistributedSmoothNodeAI.DistributedSmoothNodeAI.__init__(self, air)

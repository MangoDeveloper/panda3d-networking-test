from panda3d.core import *
from direct.distributed.DistributedObject import DistributedObject
from direct.distributed import DistributedSmoothNode
import Toon

class DistributedToon(Toon.Toon, DistributedSmoothNode.DistributedSmoothNode):
    def __init__(self, cr):
        Toon.Toon.__init__(self)
        DistributedSmoothNode.DistributedSmoothNode.__init__(self, cr)
        NodePath.__init__(self, 'Toon')

    def announceGenerate(self):
        DistributedSmoothNode.DistributedSmoothNode.announceGenerate(self)
        self.name = self.uniqueName('toon')
        self.posHprBroadcastName = self.uniqueName('toonBroadcast')
        self.toonActor.reparentTo(self)
        self.startSmooth()
        self.reparentTo(render)

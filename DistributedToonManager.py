from direct.distributed import DistributedObject

class DistributedToonManager(DistributedObject.DistributedObject):
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.cr = cr

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.cr.toonMgr = self
        messenger.send(self.cr.uniqueName('gotToonMgr'))

    def d_requestAvatar(self):
        self.sendUpdate('requestAvatar')

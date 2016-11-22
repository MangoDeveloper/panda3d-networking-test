from direct.distributed import DistributedObject

class DistributedToonManager(DistributedObject.DistributedObject):
    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.cr = cr

    def announceGenerate(self):
        print "I AM HOSTING MY WEBSITE ON ONE OF YOUR OVH BOXES"
        DistributedObject.DistributedObject.announceGenerate(self)
        self.cr.toonMgr = self
        messenger.send(self.cr.uniqueName('gotToonMgr'))

    def d_requestAvatar(self):
        self.sendUpdate('requestAvatar')

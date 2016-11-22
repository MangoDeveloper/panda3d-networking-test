from direct.distributed import DistributedObjectAI
import DistributedToonAI
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.MsgTypes import *

class DistributedToonManagerAI(DistributedObjectAI.DistributedObjectAI):
    def __init__(self, air):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)

    def announceGenerate(self):
        DistributedObjectAI.DistributedObjectAI.announceGenerate(self)
        print "HELLO COLORHOST TECHNICAL SUPPORT"

    def requestAvatar(self):
        clientId = self.air.getAvatarIdFromSender()

        player = DistributedToonAI.DistributedToonAI(self.air)
        player.generateWithRequired(2000)
        print "CREATED TOON %d" % player.doId

        self.air.setOwner(player.doId, clientId)

        self.air.clientAddSessionObject(clientId, player.doId)

        dg = PyDatagram()
        dg.addServerHeader(clientId, self.air.ourChannel, CLIENTAGENT_SET_CLIENT_ID)
        dg.addChannel(self.GetPuppetConnectionChannel(player.doId))
        self.air.send(dg)

        # self.newPlayer(player)

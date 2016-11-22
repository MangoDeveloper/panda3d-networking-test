from direct.distributed.AstronInternalRepository import AstronInternalRepository
from direct.distributed.TimeManagerAI import TimeManagerAI
from pandac.PandaModules import *
import sys
import os
import cPickle
from cStringIO import StringIO
import DistributedToonManagerAI
from hood import TTHoodDataAI
from direct.task import Task

class ToonAIRepository(AstronInternalRepository):
    def __init__(self, baseChannel, serverId, threadedNet = True):
        dcFileNames = ['direct.dc', 'toon.dc']

        self.GameGlobalsId = 1000

        AstronInternalRepository.__init__(self, baseChannel, serverId, dcFileNames = dcFileNames,
                                  dcSuffix = 'AI', connectMethod = self.CM_NET,
                                  threadedNet = threadedNet)

        # Allow some time for other processes.
        base.setSleep(0.01)

        self.games = []

        self.zoneTable = {}

        self.hoodArray = []

        self.hoods = []

        self.managerId = self.allocateChannel()
        self.toonMgrID = self.allocateChannel()

        self.zoneAllocator = UniqueIdAllocator(3, 1000000)

        tcpPort = base.config.GetInt('ai-server-port', 7199)
        hostname = base.config.GetString('ai-server-host', '127.0.0.1')
        self.acceptOnce('airConnected', self.connectSuccess)
        self.connect(hostname, tcpPort)

    def createZones(self):
        """
        Spawn safezone objects, streets, doors, NPCs, etc.
        """
        self.hoodArray.append(TTHoodDataAI.TTHoodDataAI)
        self.zoneTable[2000] = ((2000, 1, 0), (2100, 1, 1), (2200, 1, 1), (2300, 1, 1))
        self.__nextHood(0)

    def __nextHood(self, hoodIndex):
        if hoodIndex >= len(self.hoodArray):
            return Task.done

        self.hoods.append(self.hoodArray[hoodIndex](self))
        taskMgr.doMethodLater(0, ToontownAIRepository.__nextHood, 'nextHood', [self, hoodIndex + 1])
        return Task.done

    def connectSuccess(self):
        """ Successfully connected to the Message Director.
            Now to generate the TimeManagerAI """
        print 'Connected successfully!'

        self.timeManager = TimeManagerAI(self)
        self.timeManager.generateWithRequiredAndId(self.managerId, self.GameGlobalsId, 1)
        self.timeManager.setAI(self.ourChannel)
        self.districtId = self.timeManager.doId
        print "GENERATING TOON MANAGER"
        self.toonManager = DistributedToonManagerAI.DistributedToonManagerAI(self)
        self.toonManager.generateWithRequiredAndId(self.toonMgrID, self.GameGlobalsId, 1)
        self.toonManager.setAI(self.ourChannel)
        #self.makeGame()

    def lostConnection(self):
        # This should be overridden by a derived class to handle an
        # unexpectedly lost connection to the gameserver.
        self.notify.warning("Lost connection to gameserver.")
        sys.exit()

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFFL

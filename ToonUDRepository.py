from direct.distributed.AstronInternalRepository import AstronInternalRepository
from pandac.PandaModules import *
from RootObjectUD import RootObjectUD
from AvatarManagerUD import AvatarManagerUD

class ToonUDRepository(AstronInternalRepository):
    def __init__(self, threadedNet = True):
        dcFileNames = ['direct.dc', 'toon.dc']

        self.baseChannel = 100000000

        self.GameGlobalsId = 1000

        self.serverId = 4002

        AstronInternalRepository.__init__(self, self.baseChannel, self.serverId, dcFileNames = dcFileNames,
                                  dcSuffix = 'UD', connectMethod = self.CM_NET,
                                  threadedNet = threadedNet)

        # Allow some time for other processes.
        base.setSleep(0.01)

        tcpPort = base.config.GetInt('ai-server-port', 7199)
        hostname = base.config.GetString('ai-server-host', '127.0.0.1')
        self.acceptOnce('airConnected', self.connectSuccess)
        self.connect(hostname, tcpPort)


    def connectSuccess(self):
        """ Successfully connected to the Message Director.
            Now to generate the AvatarManagerAI """
        rootObj = RootObjectUD(self)
        rootObj.generateWithRequiredAndId(self.GameGlobalsId, 0, 0)
        self.setAI(self.GameGlobalsId, self.baseChannel)

        avatarManager = AvatarManagerUD(self)
        avatarManager.generateWithRequiredAndId(1001, self.GameGlobalsId, 0)

        print 'Connected successfully!'

    def getAvatarIdFromSender(self):
        return self.getMsgSender() & 0xFFFFFFFFL

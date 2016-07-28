from panda3d.core import *
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from DatagramIds import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from Toon import Toon

class ConnectionError(BaseException): pass

class ClientConnector:
    notify = DirectNotifyGlobal.directNotify.newCategory("ClientConnector")

    def __init__(self):
        self.notify.info("Client connector created.")
        self.connected = False
        self.cManager = QueuedConnectionManager()
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager,0)

        self.port_address=9099  # same for client and server
        self.ip_address="localhost"
        # how long until we give up trying to reach the server?
        self.timeout_in_miliseconds=3000  # 3 seconds
        self.serverConnection = None
        self.connect()

    def connect(self):
        self.serverConnection = self.cManager.openTCPClientConnection(self.ip_address, self.port_address, self.timeout_in_miliseconds)
        if self.serverConnection:
            self.cReader.addConnection(self.serverConnection)  # receive messages from server
        else:
            self.unableToConnect()
            return

        taskMgr.add(self.tskReaderPolling,"Poll the connection reader",-40)
        myPyDatagram = self.buildTestDatagram()  # build a datagram to send
        self.cWriter.send(myPyDatagram,self.serverConnection)
        self.heartbeat()

    def unableToConnect(self):
        raise ConnectionError("Couldn't connect to server!") # TODO: "Try again?" dialogue

    def tskReaderPolling(self, taskdata):
        if self.cReader.dataAvailable():
            datagram=NetDatagram()  # catch the incoming data in this instance
            # Check the return value; if we were threaded, someone else could have
            # snagged this data before we did
            if self.cReader.getData(datagram):
                self.myProcessDataFunction(datagram)
        return Task.cont

    def buildTestDatagram(self):
        # Send a test message
        myPyDatagram = PyDatagram()
        myPyDatagram.addUint8(PRINT_MESSAGE)
        myPyDatagram.addString(":CLIENT: Client to server connection established.")
        return myPyDatagram

    def myProcessDataFunction(self, netDatagram):
        myIterator = PyDatagramIterator(netDatagram)
        msgID = myIterator.getUint8()
        if msgID == PRINT_MESSAGE:
            messageToPrint = myIterator.getString()
            print messageToPrint
        elif msgID == HEARTBEAT:
            self.handleHeartbeat()
        elif msgID == CLOSE_CONNECTION:
            avId = myIterator.getUint64()
            base.avatars[avId].remove()
            base.avatars.pop(avId)
        elif msgID == AVATAR_LIST:
            # Each Int64 affects the remaining size by 8
            avs = myIterator.getRemainingSize() / (8 * 9) # We have 9 fields that occupy 8 units each, how many avatars do we have?
            if avs == 0: return # We have no avatars right now.
            for x in xrange(avs):
                avId = myIterator.getUint64()
                x = myIterator.getFloat64()
                y = myIterator.getFloat64()
                z = myIterator.getFloat64()
                h = myIterator.getFloat64()
                p = myIterator.getFloat64()
                r = myIterator.getFloat64()
                anim = myIterator.getString()
                playrate = myIterator.getFloat64()
                if avId == base.localAvatar.id: continue
                try:
                    base.avatars[avId]
                except:
                    base.avatars[avId] = Toon(avId = avId)
                av = base.avatars[avId].toonActor
                av.posHprInterval(0.2, (x, y, z), (h, p, r)).start()
                if av.getCurrentAnim() != anim: av.loop(anim)
                av.setPlayRate(playrate, anim)
        else:
            self.notify.warning("Unknown datagram type %d!" % msgID)

    def sendPosDatagram(self, id, x, y, z, h, p, r, anim, playrate, firstConnect = False):
        # Tell the server where we are
        try:
            base.localAvatar
        except:
            raise Exception("No localAvatar found when sending position to server!")
        posDatagram = PyDatagram()
        
        if firstConnect:
            posDatagram.addUint8(NEW_CONNECTION)
        else:
            posDatagram.addUint8(UPDATE_POS)
        posDatagram.addUint64(id)
        posDatagram.addFloat64(x)
        posDatagram.addFloat64(y)
        posDatagram.addFloat64(z)
        posDatagram.addFloat64(h)
        posDatagram.addFloat64(p)
        posDatagram.addFloat64(r)
        posDatagram.addString(anim)
        posDatagram.addFloat64(playrate)
        self.cWriter.send(posDatagram,self.serverConnection)
        return

    def closeConnection(self):
        # Going offline, let's tell the server to boot us.
        closeDG = PyDatagram()
        closeDG.addUint8(CLOSE_CONNECTION)
        closeDG.addUint64(base.localAvatar.id)
        self.cWriter.send(closeDG, self.serverConnection)
        return

    def heartbeat(self):
        posDatagram = PyDatagram()
        posDatagram.addUint8(HEARTBEAT)
        self.cWriter.send(posDatagram,self.serverConnection)
        self.notify.debug("Sent heartbeat")
        taskMgr.doMethodLater(6, self.checkHeartbeat, "Check if we got a heartbeat response") # 6 seconds seems reasonable for timing out

    def checkHeartbeat(self, task):
        if self.connected:
            self.connected = False
            self.notify.debug("Recieved heartbeat")
            self.heartbeat()
        else:
            raise ConnectionError("Server didn't respond to heartbeat!")
        return Task.done

    def handleHeartbeat(self):
        self.connected = True

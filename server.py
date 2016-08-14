from panda3d.core import *
loadPrcFileData("", "window-type none" ) # Make sure we don't need a graphics engine (Will also prevent X errors / Display errors when starting on linux without X server)
loadPrcFileData("", "audio-library-name null" ) # Prevent ALSA errors

from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.showbase import ShowBase
base = ShowBase.ShowBase()
from direct.task import Task
from DatagramIds import *
import Globals
from Toon import ServerToon

print "Networking Test -- Server"

cManager = QueuedConnectionManager()
cListener = QueuedConnectionListener(cManager, 0)
cReader = QueuedConnectionReader(cManager, 0)
cWriter = ConnectionWriter(cManager,0)

print "Connection managers created."

activeConnections=[] # We'll want to keep track of these later
avatars = {Globals.ToontownCentral: {}}
port_address=9099 #No-other TCP/IP services are using this port
backlog=1000 #If we ignore 1,000 connection attempts, something is wrong!
tcpSocket = cManager.openTCPServerRendezvous(port_address,backlog)

cListener.addConnection(tcpSocket)

print "Rendezvous port opened."

def tskListenerPolling(taskdata):
    if cListener.newConnectionAvailable():
        print "New connection available!"
        rendezvous = PointerToConnection()
        netAddress = NetAddress()
        newConnection = PointerToConnection()
    else:
        return Task.cont # nothing!

    if cListener.getNewConnection(rendezvous,netAddress,newConnection):
        newConnection = newConnection.p()
        activeConnections.append(newConnection) # Remember connection
        cReader.addConnection(newConnection)     # Begin reading connection
        print "Reading from new connection"
        sendTestDatagram(newConnection)
    return Task.cont

def tskReaderPolling(taskdata):
    if cReader.dataAvailable():
        # Note that the QueuedConnectionReader retrieves data from all clients connected to the server.
        # The NetDatagram can be queried using NetDatagram.getConnection to determine which client sent the message.
        datagram = NetDatagram()  # catch the incoming data in this instance
        # Check the return value; if we were threaded, someone else could have
        # snagged this data before we did
        if cReader.getData(datagram):
            processDatagram(datagram, datagram.getConnection())
    return Task.cont

taskMgr.add(tskListenerPolling,"Poll the connection listener",-39)
taskMgr.add(tskReaderPolling,"Poll the connection reader",-40)

def makeTestDatagram():
    # Send a test message
    testDatagram = PyDatagram()
    testDatagram.addUint8(PRINT_MESSAGE)
    testDatagram.addString(":SERVER: Server-to-client connection established.")
    return testDatagram

def processDatagram(netDatagram, connection):
    iterator = PyDatagramIterator(netDatagram)
    msgID = iterator.getUint8()
    if msgID == PRINT_MESSAGE:
        messageToPrint = iterator.getString()
        print messageToPrint
    elif msgID == HEARTBEAT:
        sendHeartbeatResponse(connection)
    elif msgID == CLOSE_CONNECTION:
        avId = iterator.getUint64()
        print "Avatar %d going offline" % avId
        avatars[Globals.ToontownCentral].pop(avId)
        activeConnections.remove(connection)
        # Tell all clients that this avatar left
        avLeftDatagram = PyDatagram()
        avLeftDatagram.addUint8(CLOSE_CONNECTION)
        avLeftDatagram.addUint64(avId)
        for client in activeConnections:
            cWriter.send(avLeftDatagram, client)
    elif msgID == UPDATE_POS:
        avId = iterator.getUint64()
        x = iterator.getFloat64()
        y = iterator.getFloat64()
        z = iterator.getFloat64()
        h = iterator.getFloat64()
        p = iterator.getFloat64()
        r = iterator.getFloat64()
        anim = iterator.getString()
        playrate = iterator.getFloat64()
        avatars[Globals.ToontownCentral][avId].x = x
        avatars[Globals.ToontownCentral][avId].y = y
        avatars[Globals.ToontownCentral][avId].z = z
        avatars[Globals.ToontownCentral][avId].h = h
        avatars[Globals.ToontownCentral][avId].p = p
        avatars[Globals.ToontownCentral][avId].r = r
        avatars[Globals.ToontownCentral][avId].anim = anim
        avatars[Globals.ToontownCentral][avId].playrate = playrate
    elif msgID == NEW_CONNECTION:
        avId = iterator.getUint64()
        x = iterator.getFloat64()
        y = iterator.getFloat64()
        z = iterator.getFloat64()
        h = iterator.getFloat64()
        p = iterator.getFloat64()
        r = iterator.getFloat64()
        anim = iterator.getString()
        playrate = iterator.getFloat64()
        avatars[Globals.ToontownCentral][avId] = ServerToon(x, y, z, h, p, r, anim, playrate)
    else:
        print "Unknown datagram type %d!" % msgID

def sendTestDatagram(connection):
    # broadcast a message to all clients
    testDatagram = makeTestDatagram()  # build a datagram to send
    cWriter.send(testDatagram, connection)

def sendHeartbeatResponse(connection):
    heartDatagram = PyDatagram()
    heartDatagram.addUint8(HEARTBEAT)
    cWriter.send(heartDatagram, connection)

def tskSendAvPos(taskdata):
    avListDG = PyDatagram()
    avListDG.addUint8(AVATAR_LIST)
    for avId in avatars[Globals.ToontownCentral]:
        av = avatars[Globals.ToontownCentral][avId]
        avListDG.addUint64(avId)
        avListDG.addFloat64(av.x)
        avListDG.addFloat64(av.y)
        avListDG.addFloat64(av.z)
        avListDG.addFloat64(av.h)
        avListDG.addFloat64(av.p)
        avListDG.addFloat64(av.r)
        avListDG.addString(av.anim)
        avListDG.addFloat64(av.playrate)
    for client in activeConnections:
        cWriter.send(avListDG, client)
    taskMgr.doMethodLater(0.25, tskSendAvPos, "Send avatar positions")
    return Task.done

taskMgr.doMethodLater(0.25, tskSendAvPos, "Send avatar positions")

def quit():
    # terminate connection to all clients
    for aClient in activeConnections:
        cReader.removeConnection(aClient)
    activeConnections=[]
        # close down our listener
    cManager.closeConnection(tcpSocket)

base.run()

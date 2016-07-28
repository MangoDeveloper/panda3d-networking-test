from panda3d.core import *
loadPrcFile("config/Config.prc")
import random
import atexit
from direct.showbase.ShowBase import ShowBase
base = ShowBase()
from direct.task import Task
import Globals
import Hood
from ClientConnector import ClientConnector
from Toon import *

# The VirtualFileSystem, which has already initialized, doesn't see the mount
# directives in the config(s) yet. We have to force it to load those manually:
from panda3d.core import VirtualFileSystem, ConfigVariableList, Filename
vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
    vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

base.connector = ClientConnector()
base.disableMouse()

base.avatars = {}

base.hoods[Globals.ToontownCentral].load()

# Create our localAvatar
base.localAvatar = LocalToon()
base.camera.reparentTo(base.localAvatar.toonActor)
base.camera.setPos(0, -15.0 - base.localAvatar.height, 1 + base.localAvatar.height)
dropPoint = random.choice(Globals.hoodDropPoints[base.currentHood])
base.localAvatar.toonActor.setPosHpr(dropPoint[0], dropPoint[1], dropPoint[2], dropPoint[3], dropPoint[4], dropPoint[5]) # Todo -- handle this depending on hood

base.connector.sendPosDatagram(base.localAvatar.id, base.localAvatar.toonActor.getX(), base.localAvatar.toonActor.getY(), base.localAvatar.toonActor.getZ(), 
                               base.localAvatar.toonActor.getH(), base.localAvatar.toonActor.getP(), base.localAvatar.toonActor.getR(), 'neutral', 1.0, firstConnect = True)
base.avatars[base.localAvatar.id] = base.localAvatar

taskMgr.add(base.localAvatar.tskSendAvPos, "Send the avatar's position to the server", -35)
atexit.register(base.connector.closeConnection) # Execute this function when logging off

base.run()

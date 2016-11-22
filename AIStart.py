from panda3d.core import *
loadPrcFileData('', 'window-type none\naudio-library-name null')
from direct.showbase import ShowBase
from ToonAIRepository import ToonAIRepository
base = ShowBase.ShowBase()
base.air = ToonAIRepository(101000000, 4002, threadedNet = True)
base.run()

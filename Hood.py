from panda3d.core import *
import Globals

class Hood:
    def __init__(self):
        self.geomFile = None
        self.skyFile = None
        self.geom = None
        self.sky = None
        self.zoneId = None

    def load(self):
        self.geom = loader.loadModel(self.geomFile)
        self.geom.reparentTo(render)
        self.geom.flattenMedium()
        self.sky = loader.loadModel(self.skyFile)
        self.sky.setTag('sky', 'Regular')
        self.sky.setScale(1.5)
        self.sky.setFogOff()
        self.sky.reparentTo(camera)
        self.sky.setZ(0.0)
        self.sky.setHpr(0.0, 0.0, 0.0)
        ce = CompassEffect.make(NodePath(), CompassEffect.PRot | CompassEffect.PZ)
        self.sky.node().setEffect(ce)
        self.sky.setTransparency(TransparencyAttrib.MDual, 1)
        base.currentHood = self.zoneId

    def unload(self):
        if self.geom:
            self.geom.removeNode()
        if self.sky:
            self.sky.removeNode()

class TTHood(Hood):
    def __init__(self):
        Hood.__init__(self)
        self.geomFile = 'phase_4/models/neighborhoods/toontown_central_full'
        self.skyFile = 'phase_3.5/models/props/TT_sky'
        self.zoneId = Globals.ToontownCentral

    def load(self):
        Hood.load(self)
        self.geom.find('**/hill').setTransparency(TransparencyAttrib.MBinary, 1)

class DDHood(Hood):
    def __init__(self):
        Hood.__init__(self)
        self.geomFile = 'phase_6/models/neighborhoods/donalds_dock'
        self.skyFile = 'phase_3.5/models/props/TT_sky'
        self.zoneId = Globals.DonaldsDock

    def load(self):
        Hood.load(self)
        self.geom.find('**/water').setTransparency(TransparencyAttrib.MDual)
        self.geom.find('**/water').setColorScale(1, 1, 1, 0.5)

base.currentHood = None
base.hoods = {Globals.ToontownCentral: TTHood()}

from direct.task import Task
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.controls.GravityWalker import GravityWalker
from direct.directnotify import DirectNotifyGlobal
import Globals, DistributedToon

class LocalToon(DistributedToon.DistributedToon):
    notify = DirectNotifyGlobal.directNotify.newCategory("LocalToon")
    def __init__(self, cr):
        DistributedToon.DistributedToon.__init__(self, cr)
        base.cTrav = CollisionTraverser()
        def getAirborneHeight():
            return offset + 0.025
        walkControls = GravityWalker(legacyLifter=True)
        walkControls.setWallBitMask(Globals.WallBitmask)
        walkControls.setFloorBitMask(Globals.FloorBitmask)
        walkControls.setWalkSpeed(16.0, 24.0, 8.0, 80.0)
        walkControls.initializeCollisions(base.cTrav, self.toonActor, floorOffset=0.025, reach=4.0)
        walkControls.setAirborneHeightFunc(getAirborneHeight)
        walkControls.enableAvatarControls()
        self.toonActor.physControls = walkControls
         
        def setWatchKey(key, input, keyMapName):
            def watchKey(active=True):
                if active == True:
                    inputState.set(input, True)
                    keyMap[keyMapName] = 1
                else:
                    inputState.set(input, False)
                    keyMap[keyMapName] = 0
            base.accept(key, watchKey, [True])
            base.accept(key+'-up', watchKey, [False])
         
        keyMap = {'left':0, 'right':0, 'forward':0, 'backward':0, 'control':0}
         
        setWatchKey('arrow_up', 'forward', 'forward')
        setWatchKey('control-arrow_up', 'forward', 'forward')
        setWatchKey('alt-arrow_up', 'forward', 'forward')
        setWatchKey('shift-arrow_up', 'forward', 'forward')
        setWatchKey('arrow_down', 'reverse', 'backward')
        setWatchKey('control-arrow_down', 'reverse', 'backward')
        setWatchKey('alt-arrow_down', 'reverse', 'backward')
        setWatchKey('shift-arrow_down', 'reverse', 'backward')
        setWatchKey('arrow_left', 'turnLeft', 'left')
        setWatchKey('control-arrow_left', 'turnLeft', 'left')
        setWatchKey('alt-arrow_left', 'turnLeft', 'left')
        setWatchKey('shift-arrow_left', 'turnLeft', 'left')
        setWatchKey('arrow_right', 'turnRight', 'right')
        setWatchKey('control-arrow_right', 'turnRight', 'right')
        setWatchKey('alt-arrow_right', 'turnRight', 'right')
        setWatchKey('shift-arrow_right', 'turnRight', 'right')
        setWatchKey('control', 'jump', 'control')

        self.movingNeutral = False
        self.movingForward = False
        self.movingRotation = False
        self.movingBackward = False
        self.movingJumping = False

        def handleMovement(task):
            if keyMap['control'] == 1:
                if keyMap['forward'] or keyMap['backward'] or keyMap['left'] or keyMap['right']:
                    if self.movingJumping == False:
                        if self.toonActor.physControls.isAirborne:
                            self.setMovementAnimation('running-jump-idle')
                        else:
                            if keyMap['forward']:
                                if self.movingForward == False:
                                    self.setMovementAnimation('run')
                            elif keyMap['backward']:
                                if self.movingBackward == False:
                                    self.setMovementAnimation('walk', playRate=-1.0)
                            elif keyMap['left'] or keyMap['right']:
                                if self.movingRotation == False:
                                    self.setMovementAnimation('walk')
                    else:
                        if not self.toonActor.physControls.isAirborne:
                            if keyMap['forward']:
                                if self.movingForward == False:
                                    self.setMovementAnimation('run')
                            elif keyMap['backward']:
                                if self.movingBackward == False:
                                    self.setMovementAnimation('walk', playRate=-1.0)
                            elif keyMap['left'] or keyMap['right']:
                                if self.movingRotation == False:
                                    self.setMovementAnimation('walk')
                else:
                    if self.movingJumping == False:
                        if self.toonActor.physControls.isAirborne:
                            self.setMovementAnimation('jump-idle')
                        else:
                            if self.movingNeutral == False:
                                self.setMovementAnimation('neutral')
                    else:
                        if not self.toonActor.physControls.isAirborne:
                            if self.movingNeutral == False:
                                self.setMovementAnimation('neutral')
            elif keyMap['forward'] == 1:
                if self.movingForward == False:
                    if not self.toonActor.physControls.isAirborne:
                        self.setMovementAnimation('run')
            elif keyMap['backward'] == 1:
                if self.movingBackward == False:
                    if not self.toonActor.physControls.isAirborne:
                        self.setMovementAnimation('walk', playRate=-1.0)
            elif keyMap['left'] or keyMap['right']:
                if self.movingRotation == False:
                    if not self.toonActor.physControls.isAirborne:
                        self.setMovementAnimation('walk')
            else:
                if not self.toonActor.physControls.isAirborne:
                    if self.movingNeutral == False:
                        self.setMovementAnimation('neutral')
            return Task.cont
         
        base.taskMgr.add(handleMovement, 'controlManager')
         
        def collisionsOn():
            self.toonActor.physControls.setCollisionsActive(True)
            self.toonActor.physControls.isAirborne = True
        def collisionsOff():
            self.toonActor.physControls.setCollisionsActive(False)
            self.toonActor.physControls.isAirborne = True
        def toggleCollisions():
            if self.toonActor.physControls.getCollisionsActive():
                self.toonActor.physControls.setCollisionsActive(False)
                self.toonActor.physControls.isAirborne = True
            else:
                self.toonActor.physControls.setCollisionsActive(True)
                self.toonActor.physControls.isAirborne = True

        base.accept('f1', toggleCollisions)
        base.accept('f2', base.oobe)

    def announceGenerate(self):
        DistributedToon.DistributedToon.announceGenerate(self)
        self.startPosHprBroadcast()
        self.d_broadcastPositionNow()
        self.startSmooth()

    def d_broadcastPositionNow(self):
        self.d_clearSmoothing()
        self.d_broadcastPosHpr()

    def setMovementAnimation(self, loopName, playRate=1.0):
        if 'jump' in loopName:
            self.movingJumping = True
            self.movingForward = False
            self.movingNeutral = False
            self.movingRotation = False
            self.movingBackward = False
        elif loopName == 'run':
            self.movingJumping = False
            self.movingForward = True
            self.movingNeutral = False
            self.movingRotation = False
            self.movingBackward = False
        elif loopName == 'walk':
            self.movingJumping = False
            self.movingForward = False
            self.movingNeutral = False
            if playRate == -1.0:
                self.movingBackward = True
                self.movingRotation = False
            else:
                self.movingBackward = False
                self.movingRotation = True
        elif loopName == 'neutral':
            self.movingJumping = False
            self.movingForward = False
            self.movingNeutral = True
            self.movingRotation = False
            self.movingBackward = False
        else:
            self.movingJumping = False
            self.movingForward = False
            self.movingNeutral = False
            self.movingRotation = False
            self.movingBackward = False
        self.toonActor.loop(loopName)
        self.toonActor.setPlayRate(playRate, loopName)

    def setZoneInformation(self, zoneId, visZones):
        """ The AI is telling us what zone we want to be in. """
        #self.cr.setInterestZones([1, 2, zoneId] + visZones)
        if self.cr.zoneInterest:
            self.cr.alterInterest(self.cr.zoneInterest, self.cr.timeManager.doId, zoneId, 'zone interest')
        else:
            self.cr.zoneInterest = self.cr.addInterest(self.cr.timeManager.doId, zoneId, 'zone interest')

        if self.cr.visInterest:
            self.cr.alterInterest(self.cr.visInterest, self.cr.timeManager.doId, visZones, 'visible interest')
        else:
            self.cr.visInterest = self.cr.addInterest(self.cr.timeManager.doId, visZones, 'visible interest')

        self.cr.locateAvatar(zoneId)

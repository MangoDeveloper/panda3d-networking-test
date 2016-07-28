from sys import argv
from direct.task import Task
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.controls.GravityWalker import GravityWalker
from direct.directnotify import DirectNotifyGlobal
import Globals

class Toon:
    notify = DirectNotifyGlobal.directNotify.newCategory("Toon")
    def __init__(self, name = "Flippy", avId = None):
        self.name = name
        self.id = id(self) if avId == None else avId

        legsAnimDict = {'right-hand-start': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_right-hand-start.bam', 'firehose': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_firehose.bam', 'rotateL-putt': 'phase_6/models/char/tt_a_chr_dgs_shorts_legs_rotateL-putt.bam', 'slip-forward': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_slip-forward.bam', 'catch-eatnrun': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_eatnrun.bam', 'tickle': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_tickle.bam', 'water-gun': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_water-gun.bam', 'leverNeutral': 'phase_10/models/char/tt_a_chr_dgs_shorts_legs_leverNeutral.bam', 'swim': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_swim.bam', 'catch-run': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_gamerun.bam', 'sad-neutral': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_sad-neutral.bam', 'pet-loop': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_petloop.bam', 'jump-squat': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-zstart.bam', 'wave': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_wave.bam', 'reel-neutral': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_reelneutral.bam', 'pole-neutral': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_poleneutral.bam', 'bank': 'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_jellybeanJar.bam', 'scientistGame': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_scientistGame.bam', 'right-hand': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_right-hand.bam', 'lookloop-putt': 'phase_6/models/char/tt_a_chr_dgs_shorts_legs_lookloop-putt.bam', 'victory': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_victory-dance.bam', 'lose': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_lose.bam', 'cringe': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_cringe.bam', 'right': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_right.bam', 'headdown-putt': 'phase_6/models/char/tt_a_chr_dgs_shorts_legs_headdown-putt.bam', 'conked': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_conked.bam', 'jump': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump.bam', 'into-putt': 'phase_6/models/char/tt_a_chr_dgs_shorts_legs_into-putt.bam', 'fish-end': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_fishEND.bam', 'running-jump-land': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_leap_zend.bam', 'shrug': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_shrug.bam', 'sprinkle-dust': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_sprinkle-dust.bam', 'hold-bottle': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_hold-bottle.bam', 'takePhone': 'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_takePhone.bam', 'melt': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_melt.bam', 'pet-start': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_petin.bam', 'look-putt': 'phase_6/models/char/tt_a_chr_dgs_shorts_legs_look-putt.bam', 'loop-putt': 'phase_6/models/char/tt_a_chr_dgs_shorts_legs_loop-putt.bam', 'good-putt': 'phase_6/models/char/tt_a_chr_dgs_shorts_legs_good-putt.bam', 'juggle': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_juggle.bam', 'run': 'phase_3/models/char/tt_a_chr_dgs_shorts_legs_run.bam', 'pushbutton': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_press-button.bam', 'sidestep-right': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-back-right.bam', 'water': 'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_water.bam', 'right-point-start': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_right-point-start.bam', 'bad-putt': 'phase_6/models/char/tt_a_chr_dgs_shorts_legs_bad-putt.bam', 'struggle': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_struggle.bam', 'running-jump': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_running-jump.bam', 'callPet': 'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_callPet.bam', 'throw': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_pie-throw.bam', 'catch-eatneutral': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_eat_neutral.bam', 'tug-o-war': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_tug-o-war.bam', 'bow': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_bow.bam', 'swing': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_swing.bam', 'climb': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_climb.bam', 'scientistWork': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_scientistWork.bam', 'think': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_think.bam', 'catch-intro-throw': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_gameThrow.bam', 'walk': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_walk.bam', 'down': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_down.bam', 'pole': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_pole.bam', 'periscope': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_periscope.bam', 'duck': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_duck.bam', 'curtsy': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_curtsy.bam', 'jump-land': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-zend.bam', 'loop-dig': 'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_loop_dig.bam', 'angry': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_angry.bam', 'bored': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_bored.bam', 'swing-putt': 'phase_6/models/char/tt_a_chr_dgs_shorts_legs_swing-putt.bam', 'pet-end': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_petend.bam', 'spit': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_spit.bam', 'right-point': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_right-point.bam', 'start-dig': 'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_into_dig.bam', 'castlong': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_castlong.bam', 'confused': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_confused.bam', 'neutral': 'phase_3/models/char/tt_a_chr_dgs_shorts_legs_neutral.bam', 'jump-idle': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_jump-zhang.bam', 'reel': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_reel.bam', 'slip-backward': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_slip-backward.bam', 'sound': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_shout.bam', 'sidestep-left': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_sidestep-left.bam', 'up': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_up.bam', 'fish-again': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_fishAGAIN.bam', 'cast': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_cast.bam', 'phoneBack': 'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_phoneBack.bam', 'phoneNeutral': 'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_phoneNeutral.bam', 'scientistJealous': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_scientistJealous.bam', 'battlecast': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_fish.bam', 'sit-start': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_intoSit.bam', 'toss': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_toss.bam', 'happy-dance': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_happy-dance.bam', 'running-jump-squat': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_leap_zstart.bam', 'teleport': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_teleport.bam', 'sit': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_sit.bam', 'sad-walk': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_losewalk.bam', 'give-props-start': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_give-props-start.bam', 'book': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_book.bam', 'running-jump-idle': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_leap_zhang.bam', 'scientistEmcee': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_scientistEmcee.bam', 'leverPull': 'phase_10/models/char/tt_a_chr_dgs_shorts_legs_leverPull.bam', 'tutorial-neutral': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_tutorial-neutral.bam', 'badloop-putt': 'phase_6/models/char/tt_a_chr_dgs_shorts_legs_badloop-putt.bam', 'give-props': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_give-props.bam', 'hold-magnet': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_hold-magnet.bam', 'hypnotize': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_hypnotize.bam', 'left-point': 'phase_3.5/models/char/tt_a_chr_dgs_shorts_legs_left-point.bam', 'leverReach': 'phase_10/models/char/tt_a_chr_dgs_shorts_legs_leverReach.bam', 'feedPet': 'phase_5.5/models/char/tt_a_chr_dgs_shorts_legs_feedPet.bam', 'reel-H': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_reelH.bam', 'applause': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_applause.bam', 'smooch': 'phase_5/models/char/tt_a_chr_dgs_shorts_legs_smooch.bam', 'rotateR-putt': 'phase_6/models/char/tt_a_chr_dgs_shorts_legs_rotateR-putt.bam', 'fish-neutral': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_fishneutral.bam', 'push': 'phase_9/models/char/tt_a_chr_dgs_shorts_legs_push.bam', 'catch-neutral': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_gameneutral.bam', 'left': 'phase_4/models/char/tt_a_chr_dgs_shorts_legs_left.bam'}
         
        torsoAnimDict = {'right-hand-start': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_right-hand-start.bam', 'firehose': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_firehose.bam', 'rotateL-putt': 'phase_6/models/char/tt_a_chr_dgl_shorts_torso_rotateL-putt.bam', 'slip-forward': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_slip-forward.bam', 'catch-eatnrun': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_eatnrun.bam', 'tickle': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_tickle.bam', 'water-gun': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_water-gun.bam', 'leverNeutral': 'phase_10/models/char/tt_a_chr_dgl_shorts_torso_leverNeutral.bam', 'swim': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_swim.bam', 'catch-run': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_gamerun.bam', 'sad-neutral': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_sad-neutral.bam', 'pet-loop': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_petloop.bam', 'jump-squat': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump-zstart.bam', 'wave': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_wave.bam', 'reel-neutral': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_reelneutral.bam', 'pole-neutral': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_poleneutral.bam', 'bank': 'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_jellybeanJar.bam', 'scientistGame': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_scientistGame.bam', 'right-hand': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_right-hand.bam', 'lookloop-putt': 'phase_6/models/char/tt_a_chr_dgl_shorts_torso_lookloop-putt.bam', 'victory': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_victory-dance.bam', 'lose': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_lose.bam', 'cringe': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_cringe.bam', 'right': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_right.bam', 'headdown-putt': 'phase_6/models/char/tt_a_chr_dgl_shorts_torso_headdown-putt.bam', 'conked': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_conked.bam', 'jump': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump.bam', 'into-putt': 'phase_6/models/char/tt_a_chr_dgl_shorts_torso_into-putt.bam', 'fish-end': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_fishEND.bam', 'running-jump-land': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_leap_zend.bam', 'shrug': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_shrug.bam', 'sprinkle-dust': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_sprinkle-dust.bam', 'hold-bottle': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_hold-bottle.bam', 'takePhone': 'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_takePhone.bam', 'melt': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_melt.bam', 'pet-start': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_petin.bam', 'look-putt': 'phase_6/models/char/tt_a_chr_dgl_shorts_torso_look-putt.bam', 'loop-putt': 'phase_6/models/char/tt_a_chr_dgl_shorts_torso_loop-putt.bam', 'good-putt': 'phase_6/models/char/tt_a_chr_dgl_shorts_torso_good-putt.bam', 'juggle': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_juggle.bam', 'run': 'phase_3/models/char/tt_a_chr_dgl_shorts_torso_run.bam', 'pushbutton': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_press-button.bam', 'sidestep-right': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump-back-right.bam', 'water': 'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_water.bam', 'right-point-start': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_right-point-start.bam', 'bad-putt': 'phase_6/models/char/tt_a_chr_dgl_shorts_torso_bad-putt.bam', 'struggle': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_struggle.bam', 'running-jump': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_running-jump.bam', 'callPet': 'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_callPet.bam', 'throw': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_pie-throw.bam', 'catch-eatneutral': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_eat_neutral.bam', 'tug-o-war': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_tug-o-war.bam', 'bow': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_bow.bam', 'swing': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_swing.bam', 'climb': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_climb.bam', 'scientistWork': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_scientistWork.bam', 'think': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_think.bam', 'catch-intro-throw': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_gameThrow.bam', 'walk': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_walk.bam', 'down': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_down.bam', 'pole': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_pole.bam', 'periscope': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_periscope.bam', 'duck': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_duck.bam', 'curtsy': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_curtsy.bam', 'jump-land': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump-zend.bam', 'loop-dig': 'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_loop_dig.bam', 'angry': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_angry.bam', 'bored': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_bored.bam', 'swing-putt': 'phase_6/models/char/tt_a_chr_dgl_shorts_torso_swing-putt.bam', 'pet-end': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_petend.bam', 'spit': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_spit.bam', 'right-point': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_right-point.bam', 'start-dig': 'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_into_dig.bam', 'castlong': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_castlong.bam', 'confused': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_confused.bam', 'neutral': 'phase_3/models/char/tt_a_chr_dgl_shorts_torso_neutral.bam', 'jump-idle': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_jump-zhang.bam', 'reel': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_reel.bam', 'slip-backward': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_slip-backward.bam', 'sound': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_shout.bam', 'sidestep-left': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_sidestep-left.bam', 'up': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_up.bam', 'fish-again': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_fishAGAIN.bam', 'cast': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_cast.bam', 'phoneBack': 'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_phoneBack.bam', 'phoneNeutral': 'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_phoneNeutral.bam', 'scientistJealous': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_scientistJealous.bam', 'battlecast': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_fish.bam', 'sit-start': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_intoSit.bam', 'toss': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_toss.bam', 'happy-dance': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_happy-dance.bam', 'running-jump-squat': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_leap_zstart.bam', 'teleport': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_teleport.bam', 'sit': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_sit.bam', 'sad-walk': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_losewalk.bam', 'give-props-start': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_give-props-start.bam', 'book': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_book.bam', 'running-jump-idle': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_leap_zhang.bam', 'scientistEmcee': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_scientistEmcee.bam', 'leverPull': 'phase_10/models/char/tt_a_chr_dgl_shorts_torso_leverPull.bam', 'tutorial-neutral': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_tutorial-neutral.bam', 'badloop-putt': 'phase_6/models/char/tt_a_chr_dgl_shorts_torso_badloop-putt.bam', 'give-props': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_give-props.bam', 'hold-magnet': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_hold-magnet.bam', 'hypnotize': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_hypnotize.bam', 'left-point': 'phase_3.5/models/char/tt_a_chr_dgl_shorts_torso_left-point.bam', 'leverReach': 'phase_10/models/char/tt_a_chr_dgl_shorts_torso_leverReach.bam', 'feedPet': 'phase_5.5/models/char/tt_a_chr_dgl_shorts_torso_feedPet.bam', 'reel-H': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_reelH.bam', 'applause': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_applause.bam', 'smooch': 'phase_5/models/char/tt_a_chr_dgl_shorts_torso_smooch.bam', 'rotateR-putt': 'phase_6/models/char/tt_a_chr_dgl_shorts_torso_rotateR-putt.bam', 'fish-neutral': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_fishneutral.bam', 'push': 'phase_9/models/char/tt_a_chr_dgl_shorts_torso_push.bam', 'catch-neutral': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_gameneutral.bam', 'left': 'phase_4/models/char/tt_a_chr_dgl_shorts_torso_left.bam'}
         
        self.mouseHead = loader.loadModel('phase_3/models/char/horse-heads-1000.bam')
        otherParts = self.mouseHead.findAllMatches('**/*long*')
        for partNum in range(0, otherParts.getNumPaths()):
            if not 'muzzle' in str(otherParts.getPath(partNum)):
                otherParts.getPath(partNum).removeNode()
        ntrlMuzzle = self.mouseHead.find('**/*muzzle*neutral')
        otherParts = self.mouseHead.findAllMatches('**/*muzzle*')
        for partNum in range(0, otherParts.getNumPaths()):
            part = otherParts.getPath(partNum)
            if part != ntrlMuzzle:
                otherParts.getPath(partNum).removeNode()
        self.mouseTorso = loader.loadModel('phase_3/models/char/tt_a_chr_dgl_shorts_torso_1000.bam')
        self.mouseLegs  = loader.loadModel('phase_3/models/char/tt_a_chr_dgs_shorts_legs_1000.bam')
        otherParts = self.mouseLegs.findAllMatches('**/boots*')+self.mouseLegs.findAllMatches('**/shoes')
        for partNum in range(0, otherParts.getNumPaths()):
            otherParts.getPath(partNum).removeNode()

        self.toonActor = Actor({'head':self.mouseHead, 'torso':self.mouseTorso, 'legs':self.mouseLegs},
                        {'torso':torsoAnimDict, 'legs':legsAnimDict})
        self.toonActor.setBlend(frameBlend = True)
        self.toonActor.attach('head', 'torso', 'def_head')
        self.toonActor.attach('torso', 'legs', 'joint_hips')

        gloves = self.toonActor.findAllMatches('**/hands')
        ears = self.toonActor.findAllMatches('**/*ears*')
        head = self.toonActor.findAllMatches('**/head-*')
        sleeves = self.toonActor.findAllMatches('**/sleeves')
        shirt = self.toonActor.findAllMatches('**/torso-top')
        shorts = self.toonActor.findAllMatches('**/torso-bot')
        neck = self.toonActor.findAllMatches('**/neck')
        arms = self.toonActor.findAllMatches('**/arms')
        legs = self.toonActor.findAllMatches('**/legs')
        feet = self.toonActor.findAllMatches('**/feet')
 
        self.bodyNodes = []
        self.bodyNodes += [gloves]
        self.bodyNodes += [head, ears]
        self.bodyNodes += [sleeves, shirt, shorts]
        self.bodyNodes += [neck, arms, legs, feet]
        self.bodyNodes[0].setColor(1, 1, 1, 1)
        self.bodyNodes[1].setColor(0.18, 0.54, 0.34, 1)
        self.bodyNodes[2].setColor(0.18, 0.54, 0.34, 1)
        self.bodyNodes[3].setColor(1, 1, 1, 1)
        self.bodyNodes[4].setColor(1, 1, 1, 1)
        self.bodyNodes[5].setColor(1, 1, 1, 1)
        self.bodyNodes[6].setColor(0.18, 0.54, 0.34, 1)
        self.bodyNodes[7].setColor(0.18, 0.54, 0.34, 1)
        self.bodyNodes[8].setColor(0.18, 0.54, 0.34, 1)
        self.bodyNodes[9].setColor(0.18, 0.54, 0.34, 1)

        topTex = loader.loadTexture('phase_4/maps/ContestfishingVestShirt2.jpg')
        botTex = loader.loadTexture('phase_4/maps/CowboyShorts1.jpg')
        sleeveTex = loader.loadTexture('phase_4/maps/ContestfishingVestSleeve1.jpg')

        self.bodyNodes[3].setTexture(sleeveTex, 1)
        self.bodyNodes[4].setTexture(topTex, 1)
        self.bodyNodes[5].setTexture(botTex, 1)
        self.toonActor.reparentTo(render)
        self.toonActor.loop('neutral')

        self.height = 3.2375

    def remove(self):
        self.toonActor.cleanup()
        self.toonActor.removeNode()
        del self

class ServerToon():
    def __init__(self, x, y, z, h, p, r, anim, playrate):
        self.x = x
        self.y = y
        self.z = z
        self.h = h
        self.p = p
        self.r = r
        self.anim = anim
        self.playrate = playrate

class LocalToon(Toon):
    notify = DirectNotifyGlobal.directNotify.newCategory("LocalToon")
    def __init__(self, name = 'Flippy'):
        Toon.__init__(self, name)
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

    def tskSendAvPos(self, taskdata):
        base.connector.sendPosDatagram(self.id, self.toonActor.getX(), self.toonActor.getY(), self.toonActor.getZ(), self.toonActor.getH(), self.toonActor.getP(), self.toonActor.getR(), self.toonActor.getCurrentAnim(), self.toonActor.getPlayRate(self.toonActor.getCurrentAnim()))
        return Task.cont

from panda3d.core import *
import os
loadPrcFile("config/Config.prc")
if os.path.isfile("resources/phase_3/audio/bgm/tt_theme.mid") and ConfigVariableBool('want-midi', True):
    # We're using midi
    loadPrcFileData("", "audio-library-name p3fmod_audio")
    bgmExt = '.mid'
    sfxExt = '.mp3' # if we have the old phase files we probably have mp3s
    sfxExt2 = '.wav' # and wavs? disney why!
else:
    # We're using ogg
    loadPrcFileData("", "audio-library-name p3openal_audio")
    bgmExt = '.ogg'
    sfxExt = sfxExt2 = '.ogg'

import atexit
import random
from direct.showbase.ShowBase import ShowBase
base = ShowBase()
from direct.task import Task
import Globals
import Hood
from Toon import *
import ToonClientRepository

# The VirtualFileSystem, which has already initialized, doesn't see the mount
# directives in the config(s) yet. We have to force it to load those manually:
vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
    vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

base.disableMouse()

base.cr = ToonClientRepository.ToonClientRepository()
base.cr.startConnect()
base.bgmExt = bgmExt
base.sfxExt = sfxExt
base.sfxExt2 = sfxExt2

base.hoods[Globals.ToontownCentral].load()

base.run()

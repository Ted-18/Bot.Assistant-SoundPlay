import os

import addons.SoundPlay.settings.settingAddon as settingAddon

def onGuildJoin(guild):
    if not os.path.exists(settingAddon.defaultSoundFolder + str(guild.id)):
            os.makedirs(settingAddon.defaultSoundFolder + str(guild.id))
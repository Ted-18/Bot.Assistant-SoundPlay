import os
import contextlib

import addons.SoundPlay.handlers.handlerSettings as handlerSettings

import services.serviceBot as serviceBot
discord = serviceBot.classBot.getDiscord()

from addons.SoundPlay.settings.settingAddon import *

if os.name == "nt":
    FFMPEG_OPTIONS = {'executable': './addons/SoundPlay/requirements/ffmpeg.exe'}
elif os.name == "posix":
    FFMPEG_OPTIONS = {'executable': './addons/SoundPlay/requirements/ffmpeg'}

class ButtonVolumeSave(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Save volume",
            style=discord.ButtonStyle.green,
            emoji="💾"
            )

    async def callback(self, interaction: discord.Interaction):

        # Get the volume from the embed field and save it to the config file
        volume = interaction.message.embeds[0].fields[0].value
        volume = volume.replace("`", "")
        volume = volume.replace("%", "")
        volume = float(volume) / 100
        
        # Save the volume in the database if the user as never set a volume, else update the volume
        if handlerSettings.getVolume(interaction.guild.id, interaction.user.id) == []:
            handlerSettings.saveVolume(interaction.guild.id, interaction.user.id, volume)
        else:
            handlerSettings.updateVolume(interaction.guild.id, interaction.user.id, volume)
        

        with contextlib.suppress(discord.HTTPException):
            await interaction.response.send_message()
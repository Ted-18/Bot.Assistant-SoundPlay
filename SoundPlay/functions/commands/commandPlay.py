import os

from addons.SoundPlay.functions.buttons.buttonPlaySound import ButtonPlaySound
from addons.SoundPlay.functions.buttons.buttonStopSound import ButtonStopSound
from addons.SoundPlay.functions.buttons.buttonVolumeLow import ButtonVolumeLow
from addons.SoundPlay.functions.buttons.buttonVolumeHigh import ButtonVolumeHigh
from addons.SoundPlay.functions.buttons.buttonVolumeSave import ButtonVolumeSave
import addons.SoundPlay.handlers.handlerSoundsList as handlerSoundsList

from addons.SoundPlay.settings.settingAddon import *

import addons.SoundPlay.handlers.handlerSettings as handlerSettings

from settings.settingColors import *


import services.serviceBot as serviceBot
discord = serviceBot.classBot.getDiscord()

async def play(ctx, directory):

    # Folder where the sounds are located
    folder = f"./addons/soundplay/sound/"

    selectedFolder = folder + str(ctx.guild.id) + "/" + directory + "/"

    # Get the folders in the folder
    dirContent = os.listdir(selectedFolder)

    # If the folder is empty, send a message
    if len(dirContent) == 0:
        embed = discord.Embed(title=f"SOUNDBOARD : {directory}", description="This folder is empty", color=red)
        await ctx.respond(embed=embed)
        return

    # Add stop button to the first view
    view = discord.ui.View(timeout=None)
    view.add_item(ButtonStopSound())

    # Add buttons to the first view
    view.add_item(ButtonVolumeLow())
    view.add_item(ButtonVolumeHigh())
    view.add_item(ButtonVolumeSave())

    # Create the embed
    embed = discord.Embed(title=f"SOUNDBOARD : {directory}", color=red)
    embed.set_footer(text="(The soundboard will be closed in 15 minutes.)")

    # Get the default volume from the database
    databaseVolume = handlerSettings.getVolume(ctx.guild.id, ctx.author.id)
    if databaseVolume == []:
        volume = defaultVolume
    else:
        volume = databaseVolume[0][0]

    embed.add_field(name="Volume", value=f"`{volume * 100:.0f}%`")


    await ctx.respond(embed=embed, view=view, delete_after=900)

    # Get the top 5 sounds played in the folder
    playSoundTopDatabase = handlerSoundsList.getAllSoundsInfo([ctx.guild.id])
    playSoundTop = []
    for sound in playSoundTopDatabase:
        if sound[0] == directory:
            playSoundTop.append(sound)

    playSoundTop.sort(key=lambda x: x[2], reverse=True)
    playSoundTop5 = playSoundTop[:5]
    

    # EN: Separate the folders into 25 buttons of 25 folders 
    # FR: S??pare les dossiers en 25 boutons de 25 dossiers
    # RU: ?????????????????? ?????????? ???? 25 ???????????? ???? 25 ??????????
    for i in range(0, len(dirContent), 25):

        # EN: Create the view
        # FR: Cr??e la vue
        # RU: ?????????????? ??????
        view = discord.ui.View(timeout=None)


        # EN: Add the buttons to the view
        # FR: Ajoute les boutons ?? la vue
        # RU: ?????????????????? ???????????? ?? ??????
        for sound in dirContent[i:i+25]:
            button = ButtonPlaySound(selectedFolder, sound)

            # EN: If the sound is in the top 5, add a star
            # FR: Si le son est dans le top 5, ajoute une ??toile
            # RU: ???????? ???????? ?? ?????? 5, ???????????????? ????????????
            for soundTop in playSoundTop5:
                if sound == soundTop[1]:
                    button.label = "??? " + button.label
                    button.style = discord.ButtonStyle.green
                    break

            view.add_item(button)

        # EN: Send the view in the channel
        # FR: Envoie la vue dans le salon
        # RU: ???????????????????? ?????? ?? ??????????
        await ctx.channel.send(view=view, delete_after=900)
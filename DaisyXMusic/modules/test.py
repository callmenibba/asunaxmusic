import os
import asyncio
import sys

from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Dialog
from pyrogram.types import Chat
from pyrogram.types import Message
from pyrogram.errors import UserAlreadyParticipant

from DaisyXMusic.services.callsmusic.callsmusic import client as USER
from DaisyXMusic.config import SUDO_USERS

@Client.on_message(filters.command(["restart"]))
async def restarting(_, message: Message):
    if message.from_user.id not in SUDO_USERS:
        return
    else:
        wtf = await message.reply("`Starting a new instance and shutting down this one`")
        
    os.system("restart.bat")
    os.execv("start.bat", sys.argv)

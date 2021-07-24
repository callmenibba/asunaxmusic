from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from DaisyXMusic.services.queues import queues
from DaisyXMusic.services.callsmusic import callsmusic

from DaisyXMusic.services.converter import converter
from DaisyXMusic.services.downloaders import youtube

from DaisyXMusic.config import BOT_NAME as bn, DURATION_LIMIT
from DaisyXMusic.helpers.filters import command, other_filters
from DaisyXMusic.helpers.decorators import errors
from DaisyXMusic.helpers.errors import DurationLimitError
from DaisyXMusic.helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(command("ply") & other_filters)
@errors
async def play(_, message: Message):

    lel = await message.reply("🔄 **Processing**")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="HE IS GAY",
                        url="https://t.me/Tamilvip007")
                   
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"This Audio is Large i can't play this"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("I need Something to play")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await lel.edit(f"#⃣ **Queued** at position {position}!")
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="https://telegra.ph/file/805db4354191f2db2f28a.jpg",
        reply_markup=keyboard,
        caption="▶️ **Playing** here the song requested by🔥{}!".format(
        message.from_user.mention()
        ),
    )
        return await lel.delete()

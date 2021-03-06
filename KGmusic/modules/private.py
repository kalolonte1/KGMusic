# Daisyxmusic (Telegram bot project )
# Copyright (C) 2021  Inukaasith

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, Chat, CallbackQuery
from KGmusic.config import SOURCE_CODE,ASSISTANT_NAME,PROJECT_NAME,SUPPORT_GROUP,UPDATES_CHANNEL,BOT_USERNAME, OWNER, BOT_NAME
logging.basicConfig(level=logging.INFO)
from KGmusic.helpers.filters import command
from time import time
from datetime import datetime
from KGmusic.helpers.decorators import authorized_users_only


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

@Client.on_message(
    filters.command(["start", f"start@{BOT_USERNAME}"])
    & filters.private
    & ~ filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>π **πͺπ²πΉπ°πΌπΊπ²** {message.from_user.mention()}**\n
π­ [BOT_NAME](https://t.me/{BOT_USERNAME}) π?πΉπΉπΌπ ππΌπ ππΌ π½πΉπ?π πΊπππΆπ° πΌπ» π΄πΏπΌππ½π ππ΅πΏπΌππ΄π΅ ππ΅π² π»π²π π§π²πΉπ²π΄πΏπ?πΊ'π ππΌπΆπ°π² π°π΅π?ππ!
π‘ ππΉπΆπ°πΈ [π΅π²πΏπ²](https://t.me/{BOT_USERNAME}?startgroup=true) ππΌ π?π±π± πΊπ² ππΌ ππΌππΏ π΄πΏπΌππ½!
<b>""",

        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "β How to use bots", callback_data="cbhelp")
                ],
                [
                   InlineKeyboardButton(
                       "π₯ Official Group", url=f"https://t.me/{SUPPORT_GROUP}"
                   ),
                   InlineKeyboardButton(
                       "π£ Updates Channel", url=f"https://t.me/aboutraks"
                   )
                ],
                [
                   InlineKeyboardButton(
                       "π οΈ Source code", url=f"https://github.com/kalolonte1/KGMusic"
                   )
                ]
            ]
        ),
        disable_web_page_preview=True
        )


@Client.on_message(
    filters.command(["start", f"start@{BOT_USERNAME}"])
    & filters.group
    & ~ filters.edited
)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""β **bot is running Successful**\n\n<b>β’ **uptime:**</b> `{uptime}`\nβ’ **start time:** `{START_TIME_ISO}`""",
        reply_markup=InlineKeyboardMarkup(
            [   
                [    
                    InlineKeyboardButton(
                        "π₯ Group", url=f"https://t.me/MusicRakaSupport"
                    ),
                    InlineKeyboardButton(
                        "βΊοΈ Channel", url=f"https://t.me/abotraks"
                    )
                ]
            ]
        )
    )

@Client.on_message(
    filters.command(["help", f"help@{BOT_USERNAME}"])
    & filters.group
    & ~ filters.edited
)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""π Hello {message.from_user.mention()} **Please** press the button below to read the **explanation** and see the list of available **Commands**\n\nOr you can directly **contact** the creator if you need **help**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "π‘ How to use bots β", callback_data=f"cbguide"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "π§βπ» Creator", url=f"https://t.me/rakaaanjayy"
                    )
                ]
            ]
        ),
    ) 

@Client.on_message(
    filters.command("reload")
    & filters.group
    & ~ filters.edited
)
async def reload(client: Client, message: Message):
    await message.reply_text("""β Bots **Successful restart!**\n\nβ **Admin list** Has been successfully **updated**""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Group Support π·οΈ", url=f"https://t.me/MusicRakaSupport"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "Channel Update π£", url=f"https://t.me/abotraks"
                    )
                ]
            ]
        ),
    ) 

@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "π `PONG!!`\n"
        f"β‘οΈ `{delta_ping * 1000:.3f} ms`"
    ) 


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@authorized_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "π€ bot status:\n"
        f"β’ **uptime:** `{uptime}`\n"
        f"β’ **start time:** `{START_TIME_ISO}`",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Group Support", url=f"https://t.me/MusicRakaSupport"
                    )
                ]
            ]
        ),
    )

import os
import asyncio
import yt_dlp

from pyrogram import Client, filters, idle
from pyrogram.types import ChatPermissions
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import MediaStream


API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

bot = Client(
    "AlphaMusicxBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

assistant = Client(
    "AlphaMusicAssistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION
)

call = PyTgCalls(assistant)

queues = {}
current = {}


def search_song(query):
    options = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        data = ydl.extract_info(
            f"ytsearch1:{query}",
            download=False
        )

    if not data.get("entries"):
        return None

    video = data["entries"][0]

    return {
        "title": video.get("title", "Unknown"),
        "url": video["url"],
        "duration": video.get("duration", 0)
    }


async def play_next(chat_id):

    if chat_id not in queues or not queues[chat_id]:
        current.pop(chat_id, None)
        return

    song = queues[chat_id].pop(0)
    current[chat_id] = song

    await call.play(
        chat_id,
        MediaStream(
            song["url"],
            video_flags=MediaStream.Flags.IGNORE
        )
    )

    return song


@bot.on_message(filters.command("start"))
async def start(_, message):

    await message.reply_text(
        "🎵 **ALPHA MUSIC**\n\n"
        "🎧 `/play song name`\n"
        "🎤 `/vplay song name`\n"
        "⏸ `/pause`\n"
        "▶️ `/resume`\n"
        "⏭ `/skip`\n"
        "⏭ `/next`\n"
        "📋 `/queue`\n"
        "⏹ `/stop`\n"
        "🔇 `/mute`\n"
        "🔊 `/unmute`\n"
        "🔊 `/volume 50`\n"
        "🚫 `/ban @user`\n"
        "✅ `/unban @user`"
    )


# ================= PLAY =================

@bot.on_message(filters.command(["play", "vplay"]))
async def play(_, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Song name likho.\n\n"
            "Example:\n"
            "`/play Tum Hi Ho`"
        )

    query = " ".join(message.command[1:])

    msg = await message.reply_text("🔎 **Searching...**")

    try:
        song = await asyncio.to_thread(search_song, query)

        if not song:
            return await msg.edit_text("❌ Song nahi mila.")

        chat_id = message.chat.id

        if chat_id not in queues:
            queues[chat_id] = []

        # Agar already song chal raha hai
        if chat_id in current:
            queues[chat_id].append(song)

            position = len(queues[chat_id])

            return await msg.edit_text(
                f"📋 **Added to Queue**\n\n"
                f"🎵 {song['title']}\n"
                f"🔢 Position: {position}"
            )

        # Pehla song
        current[chat_id] = song

        await call.play(
            chat_id,
            MediaStream(
                song["url"],
                video_flags=MediaStream.Flags.IGNORE
            )
        )

        await msg.edit_text(
            f"🎵 **Now Playing**\n\n"
            f"🎶 {song['title']}"
        )

    except Exception as e:

        await msg.edit_text(
            f"❌ **Error:**\n`{e}`"
        )


# ================= PAUSE =================

@bot.on_message(filters.command("pause"))
async def pause(_, message):

    try:
        await call.pause(message.chat.id)

        await message.reply_text(
            "⏸️ **Music Paused**"
        )

    except Exception as e:
        await message.reply_text(f"❌ `{e}`")


# ================= RESUME =================

@bot.on_message(filters.command("resume"))
async def resume(_, message):

    try:
        await call.resume(message.chat.id)

        await message.reply_text(
            "▶️ **Music Resumed**"
        )

    except Exception as e:
        await message.reply_text(f"❌ `{e}`")


# ================= SKIP =================

@bot.on_message(filters.command(["skip", "next"]))
async def skip(_, message):

    chat_id = message.chat.id

    try:

        await call.leave_call(chat_id)

        if chat_id in queues and queues[chat_id]:

            song = await play_next(chat_id)

            await message.reply_text(
                f"⏭️ **Skipped**\n\n"
                f"🎵 Next: {song['title']}"
            )

        else:

            current.pop(chat_id, None)

            await message.reply_text(
                "⏭️ **Skipped**\n\nQueue empty."
            )

    except Exception as e:

        await message.reply_text(
            f"❌ `{e}`"
        )


# ================= QUEUE =================

@bot.on_message(filters.command("queue"))
async def queue(_, message):

    chat_id = message.chat.id

    text = "📋 **ALPHA MUSIC QUEUE**\n\n"

    if chat_id in current:
        text += (
            f"🎵 **Playing:**\n"
            f"{current[chat_id]['title']}\n\n"
        )

    if chat_id in queues and queues[chat_id]:

        for i, song in enumerate(queues[chat_id][:10], 1):

            text += (
                f"{i}. {song['title']}\n"
            )

    else:

        text += "📭 Queue empty."

    await message.reply_text(text)


# ================= STOP =================

@bot.on_message(filters.command("stop"))
async def stop(_, message):

    chat_id = message.chat.id

    try:

        await call.leave_call(chat_id)

        queues.pop(chat_id, None)
        current.pop(chat_id, None)

        await message.reply_text(
            "⏹️ **Music Stopped**"
        )

    except Exception as e:

        await message.reply_text(
            f"❌ `{e}`"
        )


# ================= MUTE =================

@bot.on_message(filters.command("mute"))
async def mute(_, message):

    try:

        await call.mute(message.chat.id)

        await message.reply_text(
            "🔇 **Music Muted**"
        )

    except Exception as e:

        await message.reply_text(
            f"❌ `{e}`"
        )


# ================= UNMUTE =================

@bot.on_message(filters.command("unmute"))
async def unmute(_, message):

    try:

        await call.unmute(message.chat.id)

        await message.reply_text(
            "🔊 **Music Unmuted**"
        )

    except Exception as e:

        await message.reply_text(
            f"❌ `{e}`"
        )


# ================= VOLUME =================

@bot.on_message(filters.command("volume"))
async def volume(_, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Example: `/volume 50`"
        )

    try:

        value = int(message.command[1])

        if value < 0 or value > 200:
            return await message.reply_text(
                "❌ Volume 0 se 200 ke beech rakho."
            )

        await call.change_volume(
            message.chat.id,
            value
        )

        await message.reply_text(
            f"🔊 **Volume:** {value}%"
        )

    except Exception as e:

        await message.reply_text(
            f"❌ `{e}`"
        )


# ================= BAN =================

@bot.on_message(filters.command("ban"))
async def ban(_, message):

    if not message.reply_to_message:
        return await message.reply_text(
            "❌ Jisko ban karna hai uske message par `/ban` reply karo."
        )

    try:

        user = message.reply_to_message.from_user

        await bot.ban_chat_member(
            message.chat.id,
            user.id
        )

        await message.reply_text(
            f"🚫 **Banned:** {user.mention}"
        )

    except Exception as e:

        await message.reply_text(
            f"❌ `{e}`"
        )


# ================= UNBAN =================

@bot.on_message(filters.command("unban"))
async def unban(_, message):

    if not message.reply_to_message:
        return await message.reply_text(
            "❌ User ke message par `/unban` reply karo."
        )

    try:

        user = message.reply_to_message.from_user

        await bot.unban_chat_member(
            message.chat.id,
            user.id
        )

        await message.reply_text(
            f"✅ **Unbanned:** {user.mention}"
        )

    except Exception as e:

        await message.reply_text(
            f"❌ `{e}`"
        )


# ================= RUN =================

async def main():

    await assistant.start()
    await call.start()
    await bot.start()

    print("✅ ALPHA MUSIC STARTED")

    await idle()


if __name__ == "__main__":
    asyncio.run(main())

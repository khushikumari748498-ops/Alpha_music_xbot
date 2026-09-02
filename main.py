import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from yt_dlp import YoutubeDL
from pyrogram.types import ChatPermissions

API_ID = int(os.getenv("35483187"))
API_HASH = os.getenv("e8796df1f71abe6969b845eb8d1b57b1")
BOT_TOKEN = os.getenv("8505752014: AAF6oy7whEjP84KvI7N7Fn4LALCU3KNT1_0")
STRING_SESSION = os.getenv("BQCZzqEAUIl3gmPgLzSGMhpjBS1Oon3BEgh67a2uHFuggOBq_t70PLmOV8tXa0pbF_HloYljFcp6d_Z1xVjkcDacRz0j4jwSmJjnEq1XFcKMp2cp2ef187d06NfSrcXHv88htL1fTQq-se42zjufRvFgu16snKzzDD88yMQtRrBCGs6pUbJn5aAgjqmR9ExRnFX2FmL4diHexj48FK3qSk27mfRPR5ak74IZk7qg-aYm_GF8z4AxE_gqjmP-klAANfxFuEHwH8Pk3BoEh1CxOBuYOOTE8zxEXhrUqzmyxVtW7S5pNlN2lFf9SDx0SDD1lcZVBOtfwg37KQxMYQIPZrRQePcNLgAAAAFTjovkAA")
OWNER_ID = int(os.getenv("5696818148", "0"))

bot = Client(
    "AlphaMusicBot",
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

current_song = {}

def get_song(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)

    video = info["entries"][0]

    return {
        "title": video["title"],
        "url": video["url"]
    }

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "🎵 **ALPHA MUSIC**\n\n"
        "/play <song name> - Play\n"
        "/vplay <song name> - Play in voice chat\n"
        "/pause - Pause\n"
        "/resume - Resume\n"
        "/stop - Stop\n"
        "/mute - Mute voice chat\n"
        "/unmute - Unmute voice chat\n"
        "/skip - Skip song\n"
        "/next - Next song\n"
        "/ban <user> - Ban a user\n"
        "/unban <user> - Unban a user"
    )

@bot.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Song name लिखो। Example: `/play Tum Hi Ho`")
        return
    query = " ".join(message.command[1:])
    song = get_song(query)
    await message.reply_text(f"🎧 Playing: {song['title']} (लेकिन यह सिर्फ text feedback है, Voice Chat के लिए vplay यूज़ करें)")

@bot.on_message(filters.command("vplay"))
async def vplay(_, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Song name लिखो। Example: `/vplay Tum Hi Ho`")
        return
    query = " ".join(message.command[1:])
    msg = await message.reply_text("🔎 Song खोज रहा हूँ...")
    try:
        song = await asyncio.to_thread(get_song, query)
        await call.play(
            message.chat.id,
            MediaStream(
                song["url"],
                video_flags=MediaStream.Flags.IGNORE
            )
        )
        current_song[message.chat.id] = song
        await msg.edit_text(f"🎵 Playing: {song['title']}")
    except Exception as e:
        await msg.edit_text(f"❌ Error: `{e}`")

@bot.on_message(filters.command("pause"))
async def pause(_, message):
    try:
        await call.pause(message.chat.id)
        await message.reply_text("⏸️ Music paused.")
    except Exception as e:
        await message.reply_text(f"❌ Pause error: {e}")

@bot.on_message(filters.command("resume"))
async def resume(_, message):
    try:
        await call.resume(message.chat.id)
        await message.reply_text("▶️ Music resumed.")
    except Exception as e:
        await message.reply_text(f"❌ Resume error: {e}")

@bot.on_message(filters.command("stop"))
async def stop(_, message):
    try:
        await call.leave_call(message.chat.id)
        current_song.pop(message.chat.id, None)
        await message.reply_text("⏹️ Music stopped.")
    except Exception as e:
        await message.reply_text(f"❌ Stop error: {e}")

@bot.on_message(filters.command("mute"))
async def mute(_, message):
    try:
        await call.mute(message.chat.id)
        await message.reply_text("🔇 Voice chat muted.")
    except Exception as e:
        await message.reply_text(f"❌ Mute error: {e}")

@bot.on_message(filters.command("unmute"))
async def unmute(_, message):
    try:
        await call.unmute(message.chat.id)
        await message.reply_text("🔊 Voice chat unmuted.")
    except Exception as e:
        await message.reply_text(f"❌ Unmute error: {e}")

@bot.on_message(filters.command("skip"))
async def skip(_, message):
    # Skip logic depends on your playlist logic, here we just stop and play next.
    try:
        await call.leave_call(message.chat.id)
        await message.reply_text("⏭️ Song skipped. Play next song using /vplay <song name>.")
    except Exception as e:
        await message.reply_text(f"❌ Skip error: {e}")

@bot.on_message(filters.command("next"))
async def next_song(_, message):
    if message.chat.id in current_song:
        await message.reply_text(f"⏭️ Next song: अभी कोई नया गाना प्ले करने के लिए /vplay <song name> इस्तेमाल करें.")
    else:
        await message.reply_text("❌ कोई गाना अभी प्ले नहीं है। /vplay <song name> से शुरू करें।")

@bot.on_message(filters.command("ban"))
async def ban_user(_, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ उपयोगकर्ता का यूज़रनेम या ID बताएं। Example: `/ban @username`")

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ केवल मालिक इस कमांड का इस्तेमाल कर सकता है।")

    user = message.command[1]
    try:
        await bot.kick_chat_member(message.chat.id, user)
        await message.reply_text(f"🚫 {user} को बैन कर दिया गया।")
    except Exception as e:
        await message.reply_text(f"❌ बैन में त्रुटि: {e}")

@bot.on_message(filters.command("unban"))
async def unban_user(_, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ उपयोगकर्ता का यूज़रनेम या ID बताएं। Example: `/unban @username`")

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ केवल मालिक इस कमांड का इस्तेमाल कर सकता है।")

    user = message.command[1]
    try:
        await bot.unban_chat_member(message.chat.id, user)
        await message.reply_text(f"✅ {user} को अनबैन कर दिया गया।")
    except Exception as e:
        await message.reply_text(f"❌ अनबैन में त्रुटि: {e}")

async def main():
    await assistant.start()
    await call.start()
    await bot.start()

    print("✅ ALPHA MUSIC BOT STARTED")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())

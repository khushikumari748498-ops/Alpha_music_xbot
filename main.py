import os
import yt_dlp

from pyrogram import Client, filters, idle
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, VideoPiped

API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

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


def get_song(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(
            f"ytsearch1:{query}",
            download=False
        )

    video = info["entries"][0]

    return {
        "title": video["title"],
        "url": video["url"]
    }


@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "🎵 **ALPHA MUSIC**\n\n"
        "/play Song Name\n"
        "/pause\n"
        "/resume\n"
        "/stop"
    )


@bot.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Song name likho.\nExample: `/play Tum Hi Ho`"
        )

    query = " ".join(message.command[1:])

    try:
        await message.reply_text("🔎 Searching...")

        song = get_song(query)

        await call.play(
            message.chat.id,
            MediaStream(
                song["url"],
                video_flags=MediaStream.Flags.IGNORE
            )
        )

        await message.reply_text(
            f"🎵 **Playing:** {song['title']}"
        )

    except Exception as e:
        await message.reply_text(f"❌ Error: `{e}`")


@bot.on_message(filters.command("pause"))
async def pause(_, message):
    try:
        await call.pause(message.chat.id)
        await message.reply_text("⏸ Paused")
    except Exception as e:
        await message.reply_text(f"❌ {e}")


@bot.on_message(filters.command("resume"))
async def resume(_, message):
    try:
        await call.resume(message.chat.id)
        await message.reply_text("▶️ Resumed")
    except Exception as e:
        await message.reply_text(f"❌ {e}")


@bot.on_message(filters.command("stop"))
async def stop(_, message):
    try:
        await call.leave_call(message.chat.id)
        await message.reply_text("⏹ Stopped")
    except Exception as e:
        await message.reply_text(f"❌ {e}")


async def main():
    await assistant.start()
    await call.start()
    await bot.start()

    print("✅ ALPHA MUSIC BOT STARTED")

    await idle()

    await bot.stop()
    await assistant.stop()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

import asyncio


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

from pyrogram import Client, filters


API_ID = 35483187
API_HASH = "e8796dff7labe6969b846eb8dlb57b1"
BOT_TOKEN = "8505752014:AAF6oy7WhEjP84KvI7N7Fn4LALCu3kNTI_Q"
OWNER_ID = 5696818148
LOG_GROUP_ID = 5696818148


app = Client(
    "ALPHAMUSICX4_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hello! I am **ALPHA MUSIC BOT**. Bot successfully live ho gaya hai!")

@app.on_message(filters.command(["play", "vplay"]))
async def play_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Gane ka naam bhi likhein! Example: `/play Tum Hi Ho`")
        return
    song_name = message.text.split(None, 1)[1]
    await message.reply_text(f"🎵 **Playing:** {song_name}")

@app.on_message(filters.command(["next", "skip"]))
async def next_command(client, message):
    await message.reply_text("⏭️ **Skipped!** Agla song play ho raha hai.")

@app.on_message(filters.command("pause"))
async def pause_command(client, message):
    await message.reply_text("⏸️ Music pause ho gaya hai.")

@app.on_message(filters.command("resume"))
async def resume_command(client, message):
    await message.reply_text("▶️ Music dobara start ho gaya hai.")

@app.on_message(filters.command(["stop", "end"]))
async def stop_command(client, message):
    await message.reply_text("⏹️ Music band kar diya gaya hai aur VC disconnect ho gaya hai.")

if __name__ == "__main__":
    app.run()
    

import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioVideoPiped

# Credentials
API_ID = 38752587
API_HASH = "ef9feab27d4e8a99e0bcbeb500aff112"
BOT_TOKEN = "8021954744:AAEzgat-16tkP0kFyvfXh3a8I2LiwmAqnF0"

app = Client(
    "Alpha_music_xbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

Start Command
@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hello! I am **ALPHA MUSIC BOT**. Group me add karke kisi bhi command ka use karein.")

Play Command (/play & /vplay)
@app.on_message(filters.command(["play", "vplay"]))
async def play_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Gane ka naam bhi likhein! Example: `/play Tum Hi Ho`")
        return
    song_name = message.text.split(None, 1)[1]
    await message.reply_text(f"🎵 **Playing:** {song_name}")

Next / Skip Command
@app.on_message(filters.command(["next", "skip"]))
async def next_command(client, message):
    await message.reply_text("**Skipped!** Agla song play ho raha hai.")

 Pause Command
@app.on_message(filters.command("pause"))
async def pause_command(client, message):
    await message.reply_text("Music pause ho gaya hai.")

 Resume Command
@app.on_message(filters.command("resume"))
async def resume_command(client, message):
    await message.reply_text("Music dobara start ho gaya hai.")

Stop / End Command
@app.on_message(filters.command(["stop", "end"]))
async def stop_command(client, message):
    await message.reply_text("Music band kar diya gaya hai aur VC disconnect ho gaya hai.")

 Bot Runner Logic
async def main():
    await app.start()
    await call_py.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
   

    

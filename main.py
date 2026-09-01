import os
import asyncio
from pyrogram import Client, filters

API_ID = 2040
API_HASH = "ef9feab27d4e8a99e0bcbeb500aff112"
BOT_TOKEN = "8021954744:AAEzgat-16tkP0kFyvfXh3a8I2LiwmAqnF0"

app = Client(
    "Alpha_music_xbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hello! I am **ALPHA MUSIC BOT**.")

@app.on_message(filters.command("play"))
async def play_command(client, message):
    await message.reply_text("🎵 Playing music in Voice Chat...")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app.run()

    
    

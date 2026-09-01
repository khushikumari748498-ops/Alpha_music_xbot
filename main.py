import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

# Bot Credentials
BOT_NAME = "ALPHA ✗ MUSIC"
BOT_USERNAME = "Alpha_music_xbot"

API_ID = 123456  # my.telegram.org से API ID डालें (alphamusic)
API_HASH = "your_api_hash"
BOT_TOKEN = "8821954744:AAEzgat-l6tkP0kFyvfXh3a8I2LLweAqNf0"

app = Client("AlphaMusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("👋 Hello! I am **ALPHA MUSIC BOT**. Add me to your group and give admin rights to play music!")

@app.on_message(filters.command("play"))
async def play_command(client, message):
    await message.reply_text("🎵 Playing music in Voice Chat...")

async def main():
    await app.start()
    await call_py.start()
    print("Bot is running...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
  

import os
import re
import sys
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from yt_dlp import YoutubeDL

print("Python version:", sys.version)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    print("❌ Переменная BOT_TOKEN не задана.")
    sys.exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Отправь ссылку на видео (Instagram, YouTube, TikTok).")

@dp.message(F.text)
async def download_video(message: Message):
    url = message.text.strip()
    if not re.match(r'https?://', url):
        await message.reply("Отправь правильную ссылку.")
        return

    await message.reply("⏬ Скачиваю видео...")

    try:
        filename = "video.mp4"
        ydl_opts = {
            'outtmpl': filename,
            'format': 'best[ext=mp4]',
            'quiet': True,
            'noplaylist': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        video = FSInputFile(filename)
        await message.answer_video(video)

        os.remove(filename)

    except Exception as e:
        await message.reply(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

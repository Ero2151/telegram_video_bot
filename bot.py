import os
import re
import logging
from aiogram import Bot, Dispatcher, executor, types
from yt_dlp import YoutubeDL

API_TOKEN = os.getenv("BOT_TOKEN")
if not API_TOKEN:
    raise ValueError("BOT_TOKEN is not set!")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь ссылку на видео (YouTube, TikTok, Instagram)")

@dp.message_handler()
async def handle_video(message: types.Message):
    url = message.text.strip()
    if not re.match(r'https?://', url):
        await message.reply("Пожалуйста, отправь корректную ссылку.")
        return

    await message.reply("🔄 Скачиваю видео...")

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

        with open(filename, "rb") as video:
            await bot.send_video(message.chat.id, video)

        os.remove(filename)

    except Exception as e:
        await message.reply(f"⚠️ Ошибка: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

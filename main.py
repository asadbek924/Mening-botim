import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
import google.generativeai as genai
from aiohttp import web

# KONFIGURATSIYA
TELEGRAM_TOKEN = "8472607285:AAFt6ay6KpbZBKbUzVVn1Nov-iN1er2ft_g"
GEMINI_API_KEY = "AIzaSyAT9W7ENvrykGzEVqcvYkrCjzaV8T5OGS8"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Render uchun kichik veb-server (Port xatosini tuzatadi)
async def handle(request):
    return web.Response(text="Bot is running!")

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Salom! Men aqlli AI botman. Menga xabar yoki rasm yuboring!")

@dp.message(F.text)
async def ai_text(message: types.Message):
    response = model.generate_content(message.text)
    await message.answer(response.text)

async def main():
    # Veb serverni ishga tushirish (Render portni ko'rishi uchun)
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 5000)))
    
    print("Bot ishga tushdi...")
    await site.start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
    

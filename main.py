import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart

# KONFIGURATSIYA
TELEGRAM_TOKEN = "8796910876:AAFCBqNyb7l3bqA4E2sIIhvZm49iSd1F0uI"
GEMINI_API_KEY = "AIzaSyAT9W7ENvrykGzEVqcvYkrCjzaV8T5OGS8"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Multimedia uchun eng yaxshi model

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Salom! Men universal AI yordamchiman. Menga matn yozing, rasm yoki ovozli xabar yuboring - hammasini tushunaman! 🤖✨")

# MATNLI XABARLAR UCHUN
@dp.message(F.text)
async def ai_text(message: types.Message):
    response = model.generate_content(message.text)
    await message.answer(response.text)

# RASMLAR UCHUN (AI rasmni ko'radi)
@dp.message(F.photo)
async def ai_image(message: types.Message):
    status = await message.answer("Rasmni ko'ryapman... 👀")
    photo = await bot.get_file(message.photo[-1].file_id)
    photo_bytes = await bot.download_file(photo.file_path)
    
    img = {"mime_type": "image/jpeg", "data": photo_bytes.getvalue()}
    response = model.generate_content(["Ushbu rasmda nima borligini tushuntirib ber:", img])
    await status.edit_text(response.text)

# OVOZLI XABARLAR UCHUN (AI ovozni eshitadi)
@dp.message(F.voice)
async def ai_voice(message: types.Message):
    status = await message.answer("Ovozingizni eshityapman... 🎙")
    voice = await bot.get_file(message.voice.file_id)
    voice_bytes = await bot.download_file(voice.file_path)
    
    audio = {"mime_type": "audio/ogg", "data": voice_bytes.getvalue()}
    response = model.generate_content(["Ushbu ovozli xabarni matnga o'gir va javob ber:", audio])
    await status.edit_text(response.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

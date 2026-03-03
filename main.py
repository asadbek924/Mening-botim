import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# BOT TOKENNI @BotFather'DAN OLIB SHU YERGA QO'YING
TOKEN = "YOUR_BOT_TOKEN_HERE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 1. Asosiy Menyu (Reply Keyboard)
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🤖 Bot haqida"), types.KeyboardButton(text="📞 Aloqa"))
    builder.row(types.KeyboardButton(text="🌟 Xizmatlar"))
    return builder.as_markup(resize_keyboard=True)

# 2. Inline tugmalar
def inline_menu():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Kanalimiz", url="https://t.me/GitHub"))
    builder.row(types.InlineKeyboardButton(text="Yordam olish", callback_data="help_data"))
    return builder.as_markup()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        f"Salom {message.from_user.full_name}! Men universal yordamchiman. "
        "Menga matn, rasm, video yoki ovozli xabar yuborishingiz mumkin.",
        reply_markup=main_menu()
    )

# Matnli xabarlarga javob
@dp.message(F.text)
async def text_handler(message: types.Message):
    if message.text == "🤖 Bot haqida":
        await message.answer("Men Render hostingida 24/7 ishlovchi aqlli botman!", reply_markup=inline_menu())
    elif message.text == "📞 Aloqa":
        await message.answer("Admin bilan bog'lanish: @username")
    else:
        await message.answer(f"Siz yozdingiz: {message.text}\nTez orada javob beraman!")

# Rasmlarga javob
@dp.message(F.photo)
async def photo_handler(message: types.Message):
    await message.answer("Ajoyib rasm! Uni qabul qildim va tahlil qilyapman 🖼")

# Videolarga javob
@dp.message(F.video)
async def video_handler(message: types.Message):
    await message.answer("Video uchun rahmat! Yuklab olinyapti... 📹")

# Ovozli xabarlarga (Voice) javob
@dp.message(F.voice)
async def voice_handler(message: types.Message):
    await message.answer("Sizning ovozingizni eshitdim, juda tushunarli! 🎙")

# Inline tugma bosilganda
@dp.callback_query(F.data == "help_data")
async def help_callback(callback: types.CallbackQuery):
    await callback.answer("Yordam bo'limi yuklanmoqda...")
    await callback.message.edit_text("Sizga qanday yordam kerak? Biz barcha turdagi fayllarni qabul qilamiz.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
                             

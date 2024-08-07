from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command
import logging, asyncio
from config import token

bot = Bot(token=token)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

start_buttons = [
    [types.KeyboardButton(text='Товары'), types.KeyboardButton(text='О нас'), ],
    [types.KeyboardButton(text='Закзать'), types.KeyboardButton(text='Контакты')],
]

start_keyboard = types.ReplyKeyboardMarkup(keyboard=start_buttons, resize_keyboard=True)

@dp.message(Command("start"))
async def start(message:Message):
    await message.answer(f'Здравствуйте {message.from_user.full_name}', reply_markup=start_keyboard)

@dp.message(F.text == 'О нас')
async def about_us(message:Message):
    await message.reply("Tehno-shop - это магазин телефонов тут вы можете приобрести разные телефоны.")

@dp.message(F.text == 'Товары')
async def goods(message:Message):
    await message.reply("У нас в наличии есть iphone 15 pro, iphone 14 pro maks, sumsung a70, a также redmi 12.")

@dp.message(F.text == "Контакты")
async def contact(message:Message):
    await message.reply_contact(phone_number='+996707278553', first_name='aknazar', last_name='aknazar')

@dp.message(F.text == 'Заказать')
async def order(message:Message):
    buuton = [[types.KeyboardButton(text='Заказать', request_contact=True)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buuton, resize_keyboard=True)
    await message.reply("Пожалуйста, отправьте свои контактные данные", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
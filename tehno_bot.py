from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command
import logging, asyncio
from config import token

bot = Bot(token=token)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

start_buttons = [
    [types.KeyboardButton(text='О нас'), types.KeyboardButton(text='Товары'), ],
    [types.KeyboardButton(text='Заказать'), types.KeyboardButton(text='Контакты')],
]

start_keyboard = types.ReplyKeyboardMarkup(keyboard=start_buttons, resize_keyboard=True)


@dp.message(Command("start"))
async def start(message:Message):
    await message.answer(f'Добро пожаловать на онлайн-магазин "TEHNO-SHOP"', reply_markup=start_keyboard)

    
@dp.message(F.text == 'О нас')
async def about_us(message:Message):
    await message.reply("В нашем онлайн магазине вы можете приобрести разные товары техники.") 

@dp.message(F.text == 'Товары')
async def my_photo(message:Message):
    await message.answer_photo(photo='https://avatars.mds.yandex.net/i?id=8616052bddb2443242dc5e846041d4116bf14a9b-10930201-images-thumbs&n=13')
    await message.answer('качественное 4к тв')
    await message.reply_contact(reply_to_message_id=10)

    
@dp.message(F.text == "Контакты")
async def contact(message:Message):
    await message.answer_contact(phone_number='+996707278553', first_name='Aknazar', last_name='Umaraliev')
    
    
@dp.message(F.text == 'Заказать')
async def application(message:Message):
    buuton = [[types.KeyboardButton(text='Отправить заявку', request_contact=True)]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=buuton, resize_keyboard=True)
    await message.reply("Пожалуйста, укажите артикул товара и отправьте свои контактные данные", reply_markup=keyboard)
    
   
@dp.message(F.text == 'Назад')
async def backi(message:Message):
    await message.answer("Вы вернулись в главное меню", reply_markup=start_keyboard)
    
@dp.message(F.contact)
async def get_contact(message:Message):
    contact_info = f'Заявка на товар \nИмя: {message.contact.first_name}\nФамилия: {message.contact.last_name}\nТелефон: {message.contact.phone_number}'
    await bot.send_message(chat_id=-4281367914, text=contact_info)
    await message.answer("Спасибо, что оставили заявку")
    await message.answer('Вы вернулись на главное меню', reply_markup=start_keyboard)
    
async def main():
    await dp.start_polling(bot)
    
if __name__ == "main":
    asyncio.run(main())
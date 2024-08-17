from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from db import Database
from config import token
import logging, asyncio

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database('users.db')
db.create_table()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    username = State()
    
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.username)
    await message.reply("Привет!, Как тебя зовут ?")
    
@dp.message(Form.username, F.text)
async def process_username(message: Message, state: FSMContext):
    username = message.text
    db.add_user(message.from_user.id, username)
    await state.clear()
    await message.answer(f'Приятно познакмиться, {username}!')
    
@dp.message(Command('me'))
async def me(message: Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    if user:
        await message.answer(f"Ты зарегистрирован как {user[2]}")
    else:
        await message.answer("Ты еще не зарегистрирован")
        await start(message, state)
        
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())




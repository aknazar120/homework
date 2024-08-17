from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command

from config import token
import logging, sqlite3, time, asyncio

bot = Bot(token=token)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

connection = sqlite3.connect("users.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INT,
    username VARCHAR(100),
    note TEXT
);
""")

@dp.message(Command('start'))
async def start(message:Message):
    await message.answer(f'Привет, {message.from_user.fuii_name}, отправь мне заметку, и я ее сохраню')

@dp.message(Command('view'))
async def view_notes(message:Message):
    cursor.execute("SELECT note FROM notes WHERE id = ?"(message.from_user.id,))
    notes = cursor.fetchall()
    if notes:
        respone = '\n'.join(note[0] for note in notes)
    else:
        respone = "У вас нет заметок."
    await message.answer(respone)

@dp.message()
async def save_note(message:Message):
    cursor.execute('INSERT INTO notes (id, note) VALUES (?, ?')

async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
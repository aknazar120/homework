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
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    username VARCHAR(100),
    created VARCHAR(100)
);
""")

@dp.message(Command('start'))
async def start(message:Message):
    cursor.execute(f"SELECT id FROM users WHERE id = {message.from_user.id}")
    users_result = cursor.fetchall()
    print(users_result)
    if users_result == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?);",
                    (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, time.ctime()))
        cursor.connection.commit()
    await message.reply(f'Привет, {message.from_user.full_name}')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
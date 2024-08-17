from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import logging
import sqlite3
import asyncio
from config import token


logging.basicConfig(level=logging.INFO)


bot = Bot(token=token)
dp = Dispatcher()


def get_db_connection():
    connection = sqlite3.connect("tasks.db", check_same_thread=False)
    return connection


with get_db_connection() as connection:
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        user_id INTEGER,
        task TEXT
    );
    """)
    connection.commit()

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот для управления задачами. Используй команду /add, чтобы добавить задачу, /view — чтобы посмотреть все задачи, и /delete — чтобы удалить задачу."
    )

@dp.message(Command('add'))
async def add_task(message: types.Message):
    await message.answer("Введите задачу в следующем сообщении:")

@dp.message(Command('view'))
async def view_tasks(message: types.Message):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT task FROM tasks WHERE user_id = ?", (message.from_user.id,))
        tasks = cursor.fetchall()

    if tasks:
        response = '\n'.join([task[0] for task in tasks])
    else:
        response = "У вас нет задач."

    await message.answer(response)

@dp.message(Command('delete'))
async def delete(message: types.Message):
    with get_db_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, task FROM tasks WHERE user_id = ?", (message.from_user.id,))
        tasks = cursor.fetchall()

    if tasks:
        response = '\n'.join([f"{task[0]}. {task[1]}" for task in tasks])
        response += "\nВведите номер задачи, которую хотите удалить."
        await message.answer(response)
    else:
        await message.answer("У вас нет задач для удаления.")

@dp.message()
async def handle_message(message: types.Message):
    if message.reply_to_message:
        if 'Введите задачу в следующем сообщении' in message.reply_to_message.text:
            task_text = message.text
            logging.info(f"Attempting to add task: {task_text}")

            with get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute('INSERT INTO tasks (user_id, task) VALUES (?, ?)', (message.from_user.id, task_text))
                connection.commit()

            logging.info("Task added successfully!")
            await message.answer("Задача сохранена!")

        elif 'Введите номер задачи, которую хотите удалить' in message.reply_to_message.text:
            try:
                task_id = int(message.text)
                with get_db_connection() as connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT id FROM tasks WHERE id = ? AND user_id = ?", (task_id, message.from_user.id))
                    task = cursor.fetchone()

                    if task:
                        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                        connection.commit()
                        await message.answer("Задача удалена!")
                    else:
                        await message.answer("Задача с таким номером не найдена.")
            except ValueError:
                await message.answer("Пожалуйста, введите корректный номер задачи.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

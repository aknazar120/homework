import logging
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import asyncio
from config import API_TOKEN


SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = '@gmail.com'
SMTP_PASSWORD = ''


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

conn = sqlite3.connect('emails.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS emails
              (id INTEGER PRIMARY KEY, email TEXT, subject TEXT, message TEXT)''')
conn.commit()

class Form(StatesGroup):
    EMAIL = State()
    SUBJECT = State()
    MESSAGE = State()

@dp.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.reply("Привет! Пожалуйста, отправьте ваш Gmail адрес:")
    await state.set_state(Form.EMAIL)

@dp.message(Form.EMAIL)
async def process_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await state.set_state(Form.SUBJECT)
    await message.reply("Теперь введите тему письма:")

@dp.message(Form.SUBJECT)
async def process_subject(message: types.Message, state: FSMContext):
    subject = message.text
    await state.update_data(subject=subject)
    await state.set_state(Form.MESSAGE)
    await message.reply("И наконец, введите ваше сообщение:")

@dp.message(Form.MESSAGE)
async def process_message(message: types.Message, state: FSMContext):
    message_text = message.text
    user_data = await state.get_data()
    email = user_data['email']
    subject = user_data['subject']

    cursor.execute("INSERT INTO emails (email, subject, message) VALUES (?, ?, ?)", (email, subject, message_text))
    conn.commit()

    try:
        send_email(email, subject, message_text)
        await message.reply("Ваше сообщение успешно отправлено и сохранено в базе данных.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при отправке письма: {str(e)}")

    await state.clear()

def send_email(to_email, subject, message_text):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message_text, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, to_email, msg.as_string())

async def main():
    logger.info("Starting bot...")
    try:
        await bot.delete_webhook()
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
    finally:
        logger.info("Cleaning up...")

if name == 'main':
    asyncio.run(main())
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, BotCommand
from config import token
import requests, time, asyncio, aioschedule, logging

bot = Bot(token=token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

monitoring = False
chat_id = None

async def get_btc_price():
    url = 'https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT'
    response = requests.get(url=url).json()
    price = response.get("price")
    if price:
        return f'Стоимость биткоина на {time.ctime()}, {price}'
    else:
        return f'Не удалось получить цену биткоина'
    
async def schedule():
    while monitoring:
        message = await get_btc_price()
        await bot.send_message(chat_id, message)
        await asyncio.sleep(1)
        
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}')
    
@dp.message(Command('btc'))
async def btc(message: Message):
    global chat_id, monitoring
    chat_id = message.chat.id
    monitoring = True
    await message.answer("Начало мониторинга")
    await schedule()
    logging.info("КОМАНДА BTC АКТИВНА") 
    
    
@dp.message(Command('stop'))
async def stop(message: Message):
    global monitoring
    monitoring = False
    await message.answer("Мониторинг цены остановлен")
    
async def on():
    await bot.set_my_commands([
        BotCommand(command="/start", description='Start bot'),
        BotCommand(command="/btc", description='Start BTC monitoring'),
        BotCommand(command="/stop", description='Stop BTC monitoring'),
    ])
    logging.info("БОТ ЗАПУЩЕН")
    aioschedule.every(1).seconds.do(schedule)
    
async def main():
    dp.startup.register(on)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())

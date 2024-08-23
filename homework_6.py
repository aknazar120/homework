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

async def get_usdt_price():
    url1 = 'https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT'
    response = requests.get(url=url1).json()
    price = response.get("price")
    if price:
        return f'Стоимость биткоина USDT на {time.ctime()}, {price}'
    else:
        return f'Не удалось получить цену биткоина'
    
async def get_ethusdt_price():
    url2 = 'https://api.binance.com/api/v3/avgPrice?symbol=ETHUSDT'
    response = requests.get(url=url2).json()
    price = response.get("price")
    if price:
        return f'Стоимость биткоина ETHUSDT на {time.ctime()}, {price}'
    else:
        return f'Не удалось получить цену биткоина'
    
async def aioscheduleUSD():
    while monitoring:
        message = await get_usdt_price()
        await bot.send_message(chat_id, message)
        #await asyncio.sleep(1)
        logging.info("идет информации о текущей курс usdt")
        
async def aioscheduleETH():
    while monitoring:
        message = await get_ethusdt_price()
        await bot.send_message(chat_id, message)
        #await asyncio.sleep(1)
        logging.info("идет информации о текущей курс ethusdt")
        
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}\nкоманда: /usdt\nкоманда: /ethusdt\nкоманда: /stop')
    logging.info("КОМАНДА START АКТИВНА")

@dp.message(Command('usdt'))
async def btc(message: Message):
    global chat_id, monitoring
    chat_id = message.chat.id
    monitoring = True
    await message.answer("Начало мониторинга")
    try:
        await aioscheduleUSD()
    except:
        await message.answer('сервер не дает отчет')

    logging.info("КОМАНДА BTC АКТИВНА") 

@dp.message(Command('ethusdt'))
async def btc(message: Message):
    global chat_id, monitoring
    chat_id = message.chat.id
    monitoring = True
    await message.answer("Начало мониторинга")
    try:
        await aioscheduleETH()
    except:
        await message.answer('сервер не дает отчет')
    logging.info("КОМАНДА BTC АКТИВНА") 
    
    
@dp.message(Command('stop'))
async def stop(message: Message):
    global monitoring
    monitoring = False
    await message.answer("Мониторинг цены остановлен")
    
async def on():
    await bot.set_my_commands([
        BotCommand(command="/start", description='Start bot'),
        BotCommand(command="/usdt", description='Start USDT monitoring'),
        BotCommand(command="/ethusdt", description='Start ETHUSDT monitoring'),
        BotCommand(command="/stop", description='Stop BTC monitoring'),
    ])
    logging.info("БОТ ЗАПУЩЕН")
    aioschedule.every(10).minutes.do(aioscheduleUSD)
    aioschedule.every(10).minutes.do(aioscheduleETH)


    
async def main():
    dp.startup.register(on)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
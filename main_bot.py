import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlets import router

async def main():
    bot = Bot(token='7634357678:AAFgDfzMH2ElkGaUGkIBwNXsYkXocNmgEnE')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        KeyboardInterrupt('Бот выключен!')

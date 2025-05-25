import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlets import router

from logs import logger

async def main():
    bot = Bot(token='7634357678:AAFgDfzMH2ElkGaUGkIBwNXsYkXocNmgEnE')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


logger.info("Прогресс успешно сохранён.")
logger.error(f"Ошибка при получении заданий с ФИПИ: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        KeyboardInterrupt('Бот выключен!')

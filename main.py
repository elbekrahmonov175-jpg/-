import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database import db
from handlers import get_handlers_router


async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    
    # ПРОВЕРКА ТОКЕНА
    logging.info(f"BOT_TOKEN value: {BOT_TOKEN}")
    logging.info(f"BOT_TOKEN type: {type(BOT_TOKEN)}")
    
    if not BOT_TOKEN or BOT_TOKEN == "None":
        logging.error("BOT_TOKEN is empty! Check Railway Variables!")
        # Попробуем загрузить напрямую из окружения
        token_from_env = os.getenv("BOT_TOKEN")
        logging.info(f"Token from os.getenv: {token_from_env}")
        if token_from_env:
            logging.info("Found token in environment! Using it.")
            global BOT_TOKEN
            BOT_TOKEN = token_from_env
        else:
            logging.error("Token not found in environment either!")
            return
    
    # Инициализация базы данных
    await db.init_db()
    logging.info("Database initialized")
    
    # Создание бота и диспетчера
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Подключение роутеров
    dp.include_router(get_handlers_router())
    
    logging.info("Bot started")
    
    # Удаление вебхука и запуск polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

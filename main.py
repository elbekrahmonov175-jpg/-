import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from database import db
from handlers import get_handlers_router


async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    
    # Читаем токен из окружения
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN is empty! Check Railway Variables!")
        return
    
    logging.info(f"BOT_TOKEN loaded successfully")
    
    # Инициализация базы данных
    await db.init_db()
    logging.info("Database initialized")
    
    # Создание бота (исправлено для aiogram 3.7+)
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    
    # Создание диспетчера
    dp = Dispatcher()
    
    # Подключение роутеров
    dp.include_router(get_handlers_router())
    
    logging.info("Bot started")
    
    # Удаление вебхука и запуск polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

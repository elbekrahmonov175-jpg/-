import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from database import db
from handlers import get_handlers_router


async def main():
    # Íàñòðîéêà ëîãèðîâàíèÿ
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    
    # Èíèöèàëèçàöèÿ áàçû äàííûõ
    await db.init_db()
    logging.info("Database initialized")
    
    # Ñîçäàíèå áîòà è äèñïåò÷åðà
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Ïîäêëþ÷åíèå ðîóòåðîâ
    dp.include_router(get_handlers_router())
    
    logging.info("Bot started")
    
    # Óäàëåíèå âåáõóêà è çàïóñê polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

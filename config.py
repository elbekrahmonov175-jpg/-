import os

# Прямое чтение из окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "finance.db")

# Для отладки - можно временно раскомментировать:
# print(f"DEBUG: BOT_TOKEN loaded: {BOT_TOKEN}")

EXPENSE_CATEGORIES = ["Еда", "Транспорт", "Покупки", "Развлечения", "Коммунальные", "Другое"]
INCOME_CATEGORIES = ["Зарплата", "Бизнес", "Подарок", "Другое"]

import os

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8694365755:AAG9vRfv4MTGiacBTIT2P3eSkkIu0crXILg"
DATABASE_PATH = os.getenv("DATABASE_PATH", "finance.db")

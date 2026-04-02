import os

# Прямое чтение из окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "finance.db")

# Для отладки - можно временно раскомментировать:
# print(f"DEBUG: BOT_TOKEN loaded: {BOT_TOKEN}")

EXPENSE_CATEGORIES = ["Еда", "Транспорт", "Покупки", "Развлечения", "Коммунальные", "Другое"]
INCOME_CATEGORIES = ["Зарплата", "Бизнес", "Подарок", "Другое"]

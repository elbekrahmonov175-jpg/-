# config.py — ДОЛЖНО БЫТЬ ТАК:
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "finance.db")

EXPENSE_CATEGORIES = ["Еда", "Транспорт", "Покупки", "Развлечения", "Коммунальные", "Другое"]
INCOME_CATEGORIES = ["Зарплата", "Бизнес", "Подарок", "Другое"]

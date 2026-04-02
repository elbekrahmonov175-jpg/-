import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "finance.db")

# Êàòåãîðèè
EXPENSE_CATEGORIES = ["Åäà", "Òðàíñïîðò", "Ïîêóïêè", "Ðàçâëå÷åíèÿ", "Êîììóíàëüíûå", "Äðóãîå"]
INCOME_CATEGORIES = ["Çàðïëàòà", "Áèçíåñ", "Ïîäàðîê", "Äðóãîå"]

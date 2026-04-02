import aiosqlite
from datetime import datetime
from typing import Optional, List, Dict, Any
from config import DATABASE_PATH


class Database:
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path

    async def init_db(self):
        """Èíèöèàëèçàöèÿ áàçû äàííûõ"""
        async with aiosqlite.connect(self.db_path) as db:
            # Òàáëèöà òðàíçàêöèé
            await db.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                    category TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Òàáëèöà äîëãîâ
            await db.execute("""
                CREATE TABLE IF NOT EXISTS debts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    person_name TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('i_gave', 'i_took')),
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_paid BOOLEAN DEFAULT 0
                )
            """)
            await db.commit()

    # ============ Òðàíçàêöèè ============
    
    async def add_transaction(self, user_id: int, type_: str, category: str, amount: int):
        """Äîáàâëåíèå òðàíçàêöèè"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO transactions (user_id, type, category, amount) VALUES (?, ?, ?, ?)",
                (user_id, type_, category, amount)
            )
            await db.commit()

    async def get_balance(self, user_id: int) -> Dict[str, int]:
        """Ïîëó÷åíèå áàëàíñà ïîëüçîâàòåëÿ"""
        async with aiosqlite.connect(self.db_path) as db:
            # Îáùèé äîõîä
            cursor = await db.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = ? AND type = 'income'",
                (user_id,)
            )
            total_income = (await cursor.fetchone())[0]
            
            # Îáùèé ðàñõîä
            cursor = await db.execute(
                "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = ? AND type = 'expense'",
                (user_id,)
            )
            total_expense = (await cursor.fetchone())[0]
            
            return {
                "income": total_income,
                "expense": total_expense,
                "balance": total_income - total_expense
            }

    async def get_today_expenses(self, user_id: int) -> int:
        """Ðàñõîäû çà ñåãîäíÿ"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = ? AND type = 'expense' 
                AND date(date) = date('now', 'localtime')
            """, (user_id,))
            return (await cursor.fetchone())[0]

    async def get_month_expenses(self, user_id: int) -> int:
        """Ðàñõîäû çà òåêóùèé ìåñÿö"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT COALESCE(SUM(amount), 0) FROM transactions 
                WHERE user_id = ? AND type = 'expense' 
                AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now', 'localtime')
            """, (user_id,))
            return (await cursor.fetchone())[0]

    async def get_top_category(self, user_id: int) -> Optional[str]:
        """Ñàìàÿ ÷àñòàÿ êàòåãîðèÿ ðàñõîäîâ"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT category, COUNT(*) as cnt, SUM(amount) as total
                FROM transactions 
                WHERE user_id = ? AND type = 'expense'
                GROUP BY category
                ORDER BY cnt DESC, total DESC
                LIMIT 1
            """, (user_id,))
            result = await cursor.fetchone()
            if result:
                return f"{result[0]} ({result[1]} ðàç, {result[2]} ñóì)"
            return None

    async def get_history(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Èñòîðèÿ îïåðàöèé"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT type, category, amount, date 
                FROM transactions 
                WHERE user_id = ?
                ORDER BY date DESC
                LIMIT ?
            """, (user_id, limit))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    # ============ Äîëãè ============
    
    async def add_debt(self, user_id: int, person_name: str, amount: int, type_: str):
        """Äîáàâëåíèå äîëãà"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT INTO debts (user_id, person_name, amount, type) VALUES (?, ?, ?, ?)",
                (user_id, person_name, amount, type_)
            )
            await db.commit()

    async def get_debts(self, user_id: int, is_paid: bool = False) -> List[Dict[str, Any]]:
        """Ïîëó÷åíèå ñïèñêà äîëãîâ"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT id, person_name, amount, type, date, is_paid 
                FROM debts 
                WHERE user_id = ? AND is_paid = ?
                ORDER BY date DESC
            """, (user_id, int(is_paid)))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def mark_debt_paid(self, debt_id: int, user_id: int) -> bool:
        """Îòìåòèòü äîëã êàê îïëà÷åííûé"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "UPDATE debts SET is_paid = 1 WHERE id = ? AND user_id = ?",
                (debt_id, user_id)
            )
            await db.commit()
            return cursor.rowcount > 0

    async def get_debt_by_id(self, debt_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Ïîëó÷èòü äîëã ïî ID"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(
                "SELECT * FROM debts WHERE id = ? AND user_id = ?",
                (debt_id, user_id)
            )
            row = await cursor.fetchone()
            return dict(row) if row else None


db = Database()

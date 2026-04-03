import os
import asyncpg
from typing import Optional, List, Dict, Any

DATABASE_URL = os.getenv("DATABASE_URL")


class Database:
    def __init__(self):
        self.db_url = DATABASE_URL

    async def init_db(self):
        conn = await asyncpg.connect(self.db_url)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                type VARCHAR(10) NOT NULL,
                category VARCHAR(50) NOT NULL,
                amount INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS debts (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                person_name VARCHAR(100) NOT NULL,
                amount INTEGER NOT NULL,
                type VARCHAR(10) NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_paid BOOLEAN DEFAULT FALSE
            )
        """)
        
        await conn.close()

    async def add_transaction(self, user_id: int, type_: str, category: str, amount: int):
        conn = await asyncpg.connect(self.db_url)
        await conn.execute(
            "INSERT INTO transactions (user_id, type, category, amount) VALUES ($1, $2, $3, $4)",
            user_id, type_, category, amount
        )
        await conn.close()

    async def get_balance(self, user_id: int) -> Dict[str, int]:
        conn = await asyncpg.connect(self.db_url)
        
        row = await conn.fetchrow(
            "SELECT COALESCE(SUM(amount), 0) as total FROM transactions WHERE user_id = $1 AND type = 'income'",
            user_id
        )
        total_income = row['total']
        
        row = await conn.fetchrow(
            "SELECT COALESCE(SUM(amount), 0) as total FROM transactions WHERE user_id = $1 AND type = 'expense'",
            user_id
        )
        total_expense = row['total']
        
        await conn.close()
        
        return {
            "income": total_income,
            "expense": total_expense,
            "balance": total_income - total_expense
        }

    async def get_today_expenses(self, user_id: int) -> int:
        conn = await asyncpg.connect(self.db_url)
        row = await conn.fetchrow("""
            SELECT COALESCE(SUM(amount), 0) as total FROM transactions 
            WHERE user_id = $1 AND type = 'expense' 
            AND date::date = CURRENT_DATE
        """, user_id)
        await conn.close()
        return row['total']

    async def get_month_expenses(self, user_id: int) -> int:
        conn = await asyncpg.connect(self.db_url)
        row = await conn.fetchrow("""
            SELECT COALESCE(SUM(amount), 0) as total FROM transactions 
            WHERE user_id = $1 AND type = 'expense' 
            AND EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM CURRENT_DATE)
            AND EXTRACT(MONTH FROM date) = EXTRACT(MONTH FROM CURRENT_DATE)
        """, user_id)
        await conn.close()
        return row['total']

    async def get_top_category(self, user_id: int) -> Optional[str]:
        conn = await asyncpg.connect(self.db_url)
        row = await conn.fetchrow("""
            SELECT category, COUNT(*) as cnt, SUM(amount) as total
            FROM transactions 
            WHERE user_id = $1 AND type = 'expense'
            GROUP BY category
            ORDER BY cnt DESC, total DESC
            LIMIT 1
        """, user_id)
        await conn.close()
        
        if row:
            return f"{row['category']} ({row['cnt']} раз, {row['total']} сум)"
        return None

    async def get_history(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        conn = await asyncpg.connect(self.db_url)
        rows = await conn.fetch("""
            SELECT type, category, amount, date 
            FROM transactions 
            WHERE user_id = $1
            ORDER BY date DESC
            LIMIT $2
        """, user_id, limit)
        await conn.close()
        return [dict(row) for row in rows]

    async def add_debt(self, user_id: int, person_name: str, amount: int, type_: str):
        conn = await asyncpg.connect(self.db_url)
        await conn.execute(
            "INSERT INTO debts (user_id, person_name, amount, type) VALUES ($1, $2, $3, $4)",
            user_id, person_name, amount, type_
        )
        await conn.close()

    async def get_debts(self, user_id: int, is_paid: bool = False) -> List[Dict[str, Any]]:
        conn = await asyncpg.connect(self.db_url)
        rows = await conn.fetch("""
            SELECT id, person_name, amount, type, date, is_paid 
            FROM debts 
            WHERE user_id = $1 AND is_paid = $2
            ORDER BY date DESC
        """, user_id, is_paid)
        await conn.close()
        return [dict(row) for row in rows]

    async def mark_debt_paid(self, debt_id: int, user_id: int) -> bool:
        conn = await asyncpg.connect(self.db_url)
        result = await conn.execute(
            "UPDATE debts SET is_paid = TRUE WHERE id = $1 AND user_id = $2",
            debt_id, user_id
        )
        await conn.close()
        return result == "UPDATE 1"


db = Database()

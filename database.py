import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, List, Dict, Any

DATABASE_URL = os.getenv("DATABASE_URL")


class Database:
    def __init__(self):
        self.db_url = DATABASE_URL

    def _connect(self):
        return psycopg2.connect(self.db_url)

    async def init_db(self):
        # psycopg2 синхронный, поэтому используем обычный вызов
        conn = self._connect()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                type VARCHAR(10) NOT NULL,
                category VARCHAR(50) NOT NULL,
                amount INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cur.execute("""
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
        
        conn.commit()
        cur.close()
        conn.close()

    async def add_transaction(self, user_id: int, type_: str, category: str, amount: int):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO transactions (user_id, type, category, amount) VALUES (%s, %s, %s, %s)",
            (user_id, type_, category, amount)
        )
        conn.commit()
        cur.close()
        conn.close()

    async def get_balance(self, user_id: int) -> Dict[str, int]:
        conn = self._connect()
        cur = conn.cursor()
        
        cur.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = %s AND type = 'income'",
            (user_id,)
        )
        total_income = cur.fetchone()[0]
        
        cur.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE user_id = %s AND type = 'expense'",
            (user_id,)
        )
        total_expense = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return {
            "income": total_income,
            "expense": total_expense,
            "balance": total_income - total_expense
        }

    async def get_today_expenses(self, user_id: int) -> int:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT COALESCE(SUM(amount), 0) FROM transactions 
            WHERE user_id = %s AND type = 'expense' 
            AND date::date = CURRENT_DATE
        """, (user_id,))
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return result

    async def get_month_expenses(self, user_id: int) -> int:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT COALESCE(SUM(amount), 0) FROM transactions 
            WHERE user_id = %s AND type = 'expense' 
            AND EXTRACT(YEAR FROM date) = EXTRACT(YEAR FROM CURRENT_DATE)
            AND EXTRACT(MONTH FROM date) = EXTRACT(MONTH FROM CURRENT_DATE)
        """, (user_id,))
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return result

    async def get_top_category(self, user_id: int) -> Optional[str]:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT category, COUNT(*) as cnt, SUM(amount) as total
            FROM transactions 
            WHERE user_id = %s AND type = 'expense'
            GROUP BY category
            ORDER BY cnt DESC, total DESC
            LIMIT 1
        """, (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        
        if row:
            return f"{row[0]} ({row[1]} раз, {row[2]} сум)"
        return None

    async def get_history(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT type, category, amount, date 
            FROM transactions 
            WHERE user_id = %s
            ORDER BY date DESC
            LIMIT %s
        """, (user_id, limit))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(row) for row in rows]

    async def add_debt(self, user_id: int, person_name: str, amount: int, type_: str):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO debts (user_id, person_name, amount, type) VALUES (%s, %s, %s, %s)",
            (user_id, person_name, amount, type_)
        )
        conn.commit()
        cur.close()
        conn.close()

    async def get_debts(self, user_id: int, is_paid: bool = False) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT id, person_name, amount, type, date, is_paid 
            FROM debts 
            WHERE user_id = %s AND is_paid = %s
            ORDER BY date DESC
        """, (user_id, is_paid))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(row) for row in rows]

    async def mark_debt_paid(self, debt_id: int, user_id: int) -> bool:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "UPDATE debts SET is_paid = TRUE WHERE id = %s AND user_id = %s",
            (debt_id, user_id)
        )
        conn.commit()
        result = cur.rowcount > 0
        cur.close()
        conn.close()
        return result


db = Database()

import json
import os
from typing import Optional, List, Dict, Any
from datetime import datetime

DATA_FILE = "data/finance_data.json"


class Database:
    def __init__(self):
        self.data_file = DATA_FILE
        self._ensure_data_dir()
        self.data = self._load_data()

    def _ensure_data_dir(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

    def _load_data(self) -> dict:
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"transactions": [], "debts": []}

    def _save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    async def init_db(self):
        # JSON не нужна инициализация
        pass

    async def add_transaction(self, user_id: int, type_: str, category: str, amount: int):
        transaction = {
            "id": len(self.data["transactions"]) + 1,
            "user_id": user_id,
            "type": type_,
            "category": category,
            "amount": amount,
            "date": datetime.now().isoformat()
        }
        self.data["transactions"].append(transaction)
        self._save_data()

    async def get_balance(self, user_id: int) -> Dict[str, int]:
        user_transactions = [t for t in self.data["transactions"] if t["user_id"] == user_id]
        income = sum(t["amount"] for t in user_transactions if t["type"] == "income")
        expense = sum(t["amount"] for t in user_transactions if t["type"] == "expense")
        return {
            "income": income,
            "expense": expense,
            "balance": income - expense
        }

    async def get_today_expenses(self, user_id: int) -> int:
        today = datetime.now().date().isoformat()
        return sum(t["amount"] for t in self.data["transactions"] 
                   if t["user_id"] == user_id and t["type"] == "expense" 
                   and t["date"].startswith(today))

    async def get_month_expenses(self, user_id: int) -> int:
        month_prefix = datetime.now().strftime("%Y-%m")
        return sum(t["amount"] for t in self.data["transactions"] 
                   if t["user_id"] == user_id and t["type"] == "expense" 
                   and t["date"].startswith(month_prefix))

    async def get_top_category(self, user_id: int) -> Optional[str]:
        expenses = [t for t in self.data["transactions"] 
                    if t["user_id"] == user_id and t["type"] == "expense"]
        if not expenses:
            return None
        
        categories = {}
        for e in expenses:
            cat = e["category"]
            if cat not in categories:
                categories[cat] = {"count": 0, "total": 0}
            categories[cat]["count"] += 1
            categories[cat]["total"] += e["amount"]
        
        top = max(categories.items(), key=lambda x: (x[1]["count"], x[1]["total"]))
        return f"{top[0]} ({top[1]['count']} раз, {top[1]['total']} сум)"

    async def get_history(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        user_trans = [t for t in self.data["transactions"] if t["user_id"] == user_id]
        sorted_trans = sorted(user_trans, key=lambda x: x["date"], reverse=True)
        return sorted_trans[:limit]

    async def get_all_transactions(self, user_id: int) -> List[Dict[str, Any]]:
        """Для Excel отчёта"""
        return [t for t in self.data["transactions"] if t["user_id"] == user_id]

    async def add_debt(self, user_id: int, person_name: str, amount: int, type_: str):
        debt = {
            "id": len(self.data["debts"]) + 1,
            "user_id": user_id,
            "person_name": person_name,
            "amount": amount,
            "type": type_,
            "date": datetime.now().isoformat(),
            "is_paid": False
        }
        self.data["debts"].append(debt)
        self._save_data()

    async def get_debts(self, user_id: int, is_paid: bool = False) -> List[Dict[str, Any]]:
        return [d for d in self.data["debts"] 
                if d["user_id"] == user_id and d["is_paid"] == is_paid]

    async def mark_debt_paid(self, debt_id: int, user_id: int) -> bool:
        for debt in self.data["debts"]:
            if debt["id"] == debt_id and debt["user_id"] == user_id:
                debt["is_paid"] = True
                self._save_data()
                return True
        return False


db = Database()

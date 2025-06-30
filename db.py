import sqlite3

class DatabaseHandler:
    
    def __init__(self, db_name="finance.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
       
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL,
                    type TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    month TEXT NOT NULL
                )
            """)

    def add_transaction(self, amount, category, date, type):
       
        with self.conn:
            self.conn.execute(
                "INSERT INTO transactions (amount, category, date, type) VALUES (?, ?, ?, ?)",
                (amount, category, date, type)
            )

    def get_transactions(self, limit=50):
       
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC LIMIT ?", (limit,))
        return cursor.fetchall()

    def delete_transaction(self, transaction_id):
       
        with self.conn:
            self.conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))

    def set_budget(self, category, amount, month):
      
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM budgets WHERE category = ? AND month = ?", (category, month))
            existing = cursor.fetchone()
            if existing:
                self.conn.execute("UPDATE budgets SET amount = ? WHERE id = ?", (amount, existing[0]))
            else:
                self.conn.execute("INSERT INTO budgets (category, amount, month) VALUES (?, ?, ?)",
                                 (category, amount, month))

    def get_budget(self, category, month):
       
        cursor = self.conn.cursor()
        cursor.execute("SELECT amount FROM budgets WHERE category = ? AND month = ?", (category, month))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_category_spending(self, category, month):
        
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT SUM(amount) FROM transactions WHERE category = ? AND type = 'Expense' AND date LIKE ?",
            (category, f"{month}%")
        )
        result = cursor.fetchone()
        return result[0] or 0

    def get_summary(self, month):
        
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT type, SUM(amount) FROM transactions WHERE date LIKE ? GROUP BY type",
            (f"{month}%",)
        )
        summary = {"income": 0, "expense": 0}
        for row in cursor.fetchall():
            if row[0] == "Income":
                summary["income"] = row[1]
            elif row[0] == "Expense":
                summary["expense"] = row[1]
        return summary

    def __del__(self):
       
        self.conn.close()
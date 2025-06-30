import unittest
from logic import Transaction, Budget, CategoryManager
from db import DatabaseHandler
from datetime import datetime

class TestFinanceApp(unittest.TestCase):
   
    def setUp(self):
        """Set up test environment."""
        self.db = DatabaseHandler(":memory:")  # In-memory database for testing
        self.category_manager = CategoryManager()
        self.budget = Budget(self.db)

    def test_valid_transaction(self):
       
        trans = Transaction(100, "Food", "2025-06-12", "Expense")
        self.assertEqual(trans.amount, 100.0)
        self.assertEqual(trans.category, "Food")
        self.assertEqual(trans.type, "Expense")

    def test_invalid_amount(self):
      
        with self.assertRaises(ValueError):
            Transaction(-100, "Food", "2025-06-12", "Expense")

    def test_invalid_date(self):
        
        with self.assertRaises(ValueError):
            Transaction(100, "Food", "2025-13-01", "Expense")

    def test_invalid_category(self):
       
        with self.assertRaises(ValueError):
            self.category_manager.validate_category("Invalid")

    def test_budget_overflow(self):
        
        self.budget.set_budget("Food", 50, "2025-06")
        self.db.add_transaction(30, "Food", "2025-06-01", "Expense")
        with self.assertRaises(ValueError):
            self.budget.check_budget("Food", 30, "2025-06")

    def test_database_insert(self):
        
        self.db.add_transaction(100, "Salary", "2025-06-12", "Income")
        transactions = self.db.get_transactions()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0][1], 100.0)
        self.assertEqual(transactions[0][2], "Salary")

    def test_summary_calculation(self):
      
        self.db.add_transaction(1000, "Salary", "2025-06-01", "Income")
        self.db.add_transaction(300, "Food", "2025-06-02", "Expense")
        summary = self.db.get_summary("2025-06")
        self.assertEqual(summary["income"], 1000)
        self.assertEqual(summary["expense"], 300)

if __name__ == "__main__":
    unittest.main()
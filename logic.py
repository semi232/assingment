from datetime import datetime
import re

class Transaction:

    def __init__(self, amount, category, date, type):
        self.amount = self.validate_amount(amount)
        self.category = category
        self.date = self.validate_date(date)
        self.type = self.validate_type(type)

    @staticmethod
    def validate_amount(amount):
       
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return amount

    @staticmethod
    def validate_date(date):
       
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            raise ValueError("Date must be in YYYY-MM-DD format")
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date")
        return date

    @staticmethod
    def validate_type(type):
       
        if type not in ["Income", "Expense"]:
            raise ValueError("Type must be Income or Expense")
        return type

class Budget:
    
    def __init__(self, db):
        self.db = db

    def set_budget(self, category, amount, month):
       
        if amount <= 0:
            raise ValueError("Budget amount must be positive")
        self.db.set_budget(category, amount, month)

    def check_budget(self, category, amount, month=None):
        
        if not month:
            month = datetime.now().strftime("%Y-%m")
        budget = self.db.get_budget(category, month)
        if not budget:
            return  # No budget set
        spent = self.db.get_category_spending(category, month)
        if spent + amount > budget:
            raise ValueError(f"Budget exceeded for {category}: ${budget:.2f} allowed, ${spent + amount:.2f} spent")

class CategoryManager:
   
    def __init__(self):
        self.categories = ["Food", "Travel", "Utilities", "Entertainment", "Salary", "Other"]

    def add_category(self, category):
        
        if category and category not in self.categories:
            self.categories.append(category)

    def validate_category(self, category):
        
        if category not in self.categories:
            raise ValueError("Invalid category")
        return category

    def get_categories(self):
       
        return self.categories
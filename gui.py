import tkinter as tk
from tkinter import ttk, messagebox
from logic import Transaction, Budget, CategoryManager
from db import DatabaseHandler
from datetime import datetime

class GUIManager:
    def __init__(self, root):
        self.root = root
        self.db = DatabaseHandler()
        self.category_manager = CategoryManager()
        self.budget = Budget(self.db)
        self.root.title("Personal Finance Manager")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f8")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 10), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 10), background="#f0f4f8")
        self.style.configure("TCombobox", font=("Helvetica", 10))

        self.create_frames()

    def create_frames(self):
        self.create_home_frame()
        self.create_transaction_frame()

    def create_home_frame(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="x", pady=10)

        ttk.Label(frame, text="🏠 Home Dashboard", font=("Helvetica", 14, "bold")).pack(pady=10)
        ttk.Button(frame, text="Add Transaction", command=self.create_transaction_frame).pack(pady=10)
        ttk.Button(frame, text="View Recent Transactions", command=self.update_transaction_list).pack(pady=10)

    def create_transaction_frame(self):
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="x", pady=10)

        ttk.Label(frame, text="➕ Add New Transaction", font=("Helvetica", 14, "bold")).pack(pady=10)

        form_frame = ttk.Frame(frame)
        form_frame.pack(fill="x")

        ttk.Label(form_frame, text="Amount").grid(row=0, column=0, sticky="w")
        self.amount_entry = ttk.Entry(form_frame)
        self.amount_entry.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Category").grid(row=1, column=0, sticky="w")
        self.category_combobox = ttk.Combobox(form_frame, values=self.category_manager.get_categories())
        self.category_combobox.grid(row=1, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="w")
        self.date_entry = ttk.Entry(form_frame)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=2, column=1, pady=5, sticky="ew")

        ttk.Label(form_frame, text="Type").grid(row=3, column=0, sticky="w")
        self.type_var = tk.StringVar(value="Expense")
        ttk.Radiobutton(form_frame, text="Income", variable=self.type_var, value="Income").grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(form_frame, text="Expense", variable=self.type_var, value="Expense").grid(row=3, column=2, sticky="w")

        ttk.Button(frame, text="Submit Transaction", command=self.add_transaction).pack(pady=10)

        form_frame.columnconfigure(1, weight=1)

        # Transaction list
        self.transaction_listbox = tk.Listbox(frame, width=50, height=10)
        self.transaction_listbox.pack(pady=10)
        ttk.Button(frame, text="Delete Selected", command=self.delete_transaction).pack(pady=5)
        self.update_transaction_list()

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_combobox.get()
            date = self.date_entry.get()
            type = self.type_var.get()

            Transaction.validate_amount(amount)
            self.category_manager.validate_category(category)
            Transaction.validate_date(date)

            if type == "Expense":
                self.budget.check_budget(category, amount)

            self.db.add_transaction(amount, category, date, type)
            messagebox.showinfo("Success", "Transaction added!")
            self.update_transaction_list()
            self.clear_inputs()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def delete_transaction(self):
        try:
            selected = self.transaction_listbox.curselection()
            if not selected:
                raise ValueError("No transaction selected")
            transaction_id = int(self.transaction_listbox.get(selected[0]).split("ID: ")[1].split(",")[0])
            self.db.delete_transaction(transaction_id)
            messagebox.showinfo("Success", "Transaction deleted")
            self.update_transaction_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_transaction_list(self):
        if not hasattr(self, 'transaction_listbox'):
            return
        self.transaction_listbox.delete(0, tk.END)
        transactions = self.db.get_transactions()
        for t in transactions:
            self.transaction_listbox.insert(tk.END, f"ID: {t[0]}, {t[4]}: ${t[1]:.2f}, {t[2]}, {t[3]}")

    def clear_inputs(self):
        self.amount_entry.delete(0, tk.END)
        self.category_combobox.set("")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

#!/usr/bin/env python3
"""
Personal Budget and Expense Tracker
==================================

This script provides an interactive command‑line interface for managing
personal finances. It allows users to create spending categories,
record income and expense transactions, view detailed listings and
summaries, and generate basic monthly reports. Data is persisted in a
SQLite database so that information is saved between runs.

Features:

* Create, list and delete categories for classifying transactions
* Record transactions with date, amount, description and category
* List transactions with optional filters (by category or date range)
* Compute monthly summary reports grouped by category
* Export transactions to a CSV file

Usage:
    python budget_tracker.py

The program presents a menu. Enter the number corresponding to
the desired action. Press Ctrl+C at any time to exit gracefully.
"""

import csv
import os
import sqlite3
from contextlib import closing
from datetime import datetime
from typing import Optional, List, Tuple


DB_FILE = "budget.db"


class BudgetDB:
    """Encapsulate database access for categories and transactions."""

    def __init__(self, filename: str = DB_FILE) -> None:
        self.filename = filename
        self.conn = sqlite3.connect(self.filename)
        # Ensure foreign keys are enforced
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        """Create tables if they do not exist."""
        with closing(self.conn.cursor()) as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    category_id INTEGER,
                    type TEXT NOT NULL CHECK(type IN ('income','expense')),
                    FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE SET NULL
                )
                """
            )
        self.conn.commit()

    # Category operations
    def add_category(self, name: str) -> int:
        """Insert a new category and return its ID."""
        with closing(self.conn.cursor()) as cur:
            cur.execute("INSERT INTO categories (name) VALUES (?)", (name.strip(),))
            self.conn.commit()
            return cur.lastrowid

    def delete_category(self, category_id: int) -> bool:
        """Delete a category by ID. Returns True if a row was removed."""
        with closing(self.conn.cursor()) as cur:
            cur.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            self.conn.commit()
            return cur.rowcount > 0

    def list_categories(self) -> List[Tuple[int, str]]:
        """Return all categories as a list of (id, name)."""
        with closing(self.conn.cursor()) as cur:
            cur.execute("SELECT id, name FROM categories ORDER BY name")
            return cur.fetchall()

    # Transaction operations
    def add_transaction(
        self,
        date: str,
        amount: float,
        description: str,
        category_id: Optional[int],
        txn_type: str,
    ) -> int:
        """Insert a new transaction and return its ID."""
        with closing(self.conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO transactions (date, amount, description, category_id, type) VALUES (?, ?, ?, ?, ?)",
                (date, amount, description.strip(), category_id, txn_type),
            )
            self.conn.commit()
            return cur.lastrowid

    def delete_transaction(self, txn_id: int) -> bool:
        """Delete a transaction by ID."""
        with closing(self.conn.cursor()) as cur:
            cur.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
            self.conn.commit()
            return cur.rowcount > 0

    def list_transactions(
        self,
        category_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Tuple[int, str, float, str, Optional[int], str]]:
        """Retrieve transactions with optional filters."""
        query = "SELECT id, date, amount, description, category_id, type FROM transactions"
        clauses = []
        params: List = []
        if category_id:
            clauses.append("category_id = ?")
            params.append(category_id)
        if start_date:
            clauses.append("date >= ?")
            params.append(start_date)
        if end_date:
            clauses.append("date <= ?")
            params.append(end_date)
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY date DESC, id DESC"
        with closing(self.conn.cursor()) as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def monthly_summary(self, year: int, month: int) -> List[Tuple[str, float, float]]:
        """Return income and expense totals by category for a given month."""
        start = f"{year:04d}-{month:02d}-01"
        # Compute end-of-month; simple approach: next month minus 1 day
        if month == 12:
            end_year, end_month = year + 1, 1
        else:
            end_year, end_month = year, month + 1
        end = f"{end_year:04d}-{end_month:02d}-01"
        query = (
            "SELECT c.name, "
            "SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END) AS income_total, "
            "SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END) AS expense_total "
            "FROM transactions t "
            "LEFT JOIN categories c ON t.category_id = c.id "
            "WHERE t.date >= ? AND t.date < ? "
            "GROUP BY c.name"
        )
        with closing(self.conn.cursor()) as cur:
            cur.execute(query, (start, end))
            return cur.fetchall()

    def export_to_csv(
        self,
        filename: str,
        category_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> None:
        """Export filtered transactions to a CSV file."""
        rows = self.list_transactions(category_id, start_date, end_date)
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["ID", "Date", "Amount", "Description", "CategoryID", "Type"])
            writer.writerows(rows)

    def close(self) -> None:
        self.conn.close()



def prompt(text: str) -> str:
    """Prompt the user for input and return the stripped string."""
    return input(text).strip()



def print_categories(categories: List[Tuple[int, str]]) -> None:
    if not categories:
        print("No categories defined.")
        return
    print(f"{'ID':<4} Name")
    print("-" * 30)
    for cid, name in categories:
        print(f"{cid:<4} {name}")



def print_transactions(
    rows: List[Tuple[int, str, float, str, Optional[int], str]], categories: List[Tuple[int, str]]
) -> None:
    cat_lookup = {cid: name for cid, name in categories}
    if not rows:
        print("No transactions found.")
        return
    header = f"{'ID':<4} {'Date':<10} {'Type':<7} {'Amount':<10} {'Category':<15} Description"
    print(header)
    print("-" * len(header))
    for tid, date, amount, desc, cid, txn_type in rows:
        cat_name = cat_lookup.get(cid, "(uncategorized)")
        print(f"{tid:<4} {date:<10} {txn_type:<7} {amount:<10.2f} {cat_name:<15} {desc}")



def add_category_flow(db: BudgetDB) -> None:
    name = prompt("Enter new category name: ")
    if not name:
        print("Category name cannot be empty.")
        return
    try:
        cid = db.add_category(name)
        print(f"Category '{name}' added with ID {cid}.")
    except sqlite3.IntegrityError:
        print(f"Category '{name}' already exists.")



def delete_category_flow(db: BudgetDB) -> None:
    try:
        cid = int(prompt("Enter category ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return
    if db.delete_category(cid):
        print(f"Category #{cid} deleted. Transactions remain but become uncategorized.")
    else:
        print(f"Category #{cid} not found.")



def add_transaction_flow(db: BudgetDB) -> None:
    date_str = prompt("Enter date (YYYY-MM-DD): ")
    try:
        # Validate date format
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_iso = date_obj.date().isoformat()
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return
    try:
        amount = float(prompt("Enter amount (positive for income, negative for expense): "))
    except ValueError:
        print("Amount must be a number.")
        return
    description = prompt("Enter description: ")
    # Determine type based on sign
    txn_type = "income" if amount >= 0 else "expense"
    abs_amount = abs(amount)
    categories = db.list_categories()
    print_categories(categories)
    cat_input = prompt("Enter category ID or leave blank for uncategorized: ")
    if cat_input:
        try:
            category_id = int(cat_input)
        except ValueError:
            print("Invalid category ID. Transaction not saved.")
            return
    else:
        category_id = None
    txn_id = db.add_transaction(date_iso, abs_amount, description, category_id, txn_type)
    print(f"Transaction #{txn_id} recorded.")



def delete_transaction_flow(db: BudgetDB) -> None:
    try:
        tid = int(prompt("Enter transaction ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return
    if db.delete_transaction(tid):
        print(f"Transaction #{tid} deleted.")
    else:
        print(f"Transaction #{tid} not found.")



def list_transactions_flow(db: BudgetDB) -> None:
    categories = db.list_categories()
    print_categories(categories)
    cat_input = prompt("Filter by category ID (or leave blank): ")
    category_id = None
    if cat_input:
        try:
            category_id = int(cat_input)
        except ValueError:
            print("Invalid category ID. Showing all transactions.")
    start = prompt("Start date (YYYY-MM-DD) or leave blank: ") or None
    end = prompt("End date (YYYY-MM-DD) or leave blank: ") or None
    try:
        # Validate date formats if provided
        if start:
            datetime.strptime(start, "%Y-%m-%d")
        if end:
            datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return
    rows = db.list_transactions(category_id, start, end)
    print_transactions(rows, categories)



def monthly_summary_flow(db: BudgetDB) -> None:
    try:
        year = int(prompt("Enter year (YYYY): "))
        month = int(prompt("Enter month (1-12): "))
        if month < 1 or month > 12:
            raise ValueError
    except ValueError:
        print("Invalid year or month.")
        return
    summary = db.monthly_summary(year, month)
    if not summary:
        print("No transactions found for the given month.")
        return
    print(f"Summary for {year}-{month:02d}")
    print(f"{'Category':<20} {'Income':<10} {'Expense':<10} {'Net':<10}")
    print("-" * 60)
    for cat_name, income_total, expense_total in summary:
        # cat_name may be None if uncategorized
        name = cat_name or "(uncategorized)"
        net = (income_total or 0) - (expense_total or 0)
        print(f"{name:<20} {income_total or 0:<10.2f} {expense_total or 0:<10.2f} {net:<10.2f}")



def export_csv_flow(db: BudgetDB) -> None:
    filename = prompt("Enter filename to export to (e.g. report.csv): ")
    if not filename:
        print("Filename cannot be empty.")
        return
    categories = db.list_categories()
    print_categories(categories)
    cat_input = prompt("Filter by category ID (or leave blank): ")
    category_id = None
    if cat_input:
        try:
            category_id = int(cat_input)
        except ValueError:
            print("Invalid category ID. Exporting all categories.")
    start = prompt("Start date (YYYY-MM-DD) or leave blank: ") or None
    end = prompt("End date (YYYY-MM-DD) or leave blank: ") or None
    try:
        if start:
            datetime.strptime(start, "%Y-%m-%d")
        if end:
            datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return
    db.export_to_csv(filename, category_id, start, end)
    print(f"Transactions exported to {filename}.")



def menu() -> None:
    print("\nBudget Tracker")
    print("1. Add category")
    print("2. Delete category")
    print("3. Add transaction")
    print("4. Delete transaction")
    print("5. List transactions")
    print("6. Monthly summary")
    print("7. Export transactions to CSV")
    print("8. Exit")



def main() -> None:
    db = BudgetDB()
    try:
        while True:
            menu()
            choice = prompt("Select an option (1-8): ")
            if choice == "1":
                add_category_flow(db)
            elif choice == "2":
                delete_category_flow(db)
            elif choice == "3":
                add_transaction_flow(db)
            elif choice == "4":
                delete_transaction_flow(db)
            elif choice == "5":
                list_transactions_flow(db)
            elif choice == "6":
                monthly_summary_flow(db)
            elif choice == "7":
                export_csv_flow(db)
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please enter a number between 1 and 8.")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        db.close()



if __name__ == "__main__":
    main()

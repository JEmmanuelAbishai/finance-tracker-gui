import sqlite3
import os

# Use absolute path for DB_PATH
DB_PATH = os.path.abspath(
    os.path.join("data", "finance_tracker.db")
)

# Ensure the 'data' folder exists
os.makedirs("data", exist_ok=True)


def connect_db():
    """Connect to the SQLite database."""

    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, timeout=10)


def create_table():
    """Create the transactions table if it does not exist."""

    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                amount REAL
            )
        """)

        conn.commit()


def add_transaction(date, category, amount):
    """Insert a transaction into the database."""

    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO transactions (date, category, amount)
            VALUES (?, ?, ?)
            """,
            (date, category, amount)
        )

        conn.commit()


def get_transactions():
    """Retrieve all transactions."""

    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()

        return transactions


def reset_transactions():
    """Clear all transaction records but keep the table structure."""

    with connect_db() as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM transactions")
        conn.commit()

    print("All previous transactions have been cleared.")


# Create the table when this file is run/imported
create_table()
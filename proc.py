import pandas as pd
import os
import sqlite3

# Use absolute path for DB_PATH
DB_PATH = os.path.abspath(
    os.path.join("data", "finance_tracker.db")
)


def connect_db():
    """Connect to the SQLite database."""

    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH, timeout=10)


def load_transactions():
    """Load transactions from the database into a DataFrame."""

    conn = connect_db()

    try:
        df = pd.read_sql_query(
            "SELECT * FROM transactions",
            conn
        )
    finally:
        conn.close()

    # Convert date column to datetime
    if "date" in df.columns:
        try:
            # Try the common YYYY-MM-DD format first
            df["date"] = pd.to_datetime(
                df["date"],
                format="%Y-%m-%d",
                errors="coerce"
            )

            # If all dates failed, try DD-MM-YYYY
            if df["date"].isna().all():
                df["date"] = pd.to_datetime(
                    df["date"],
                    format="%d-%m-%Y",
                    errors="coerce"
                )

        except Exception as e:
            print("Date conversion error:", e)

    # Remove rows with invalid dates
    if "date" in df.columns:
        df = df.dropna(subset=["date"])

    return df


def get_expense_by_category():
    """Calculate total spending per category."""

    df = load_transactions()

    if df.empty:
        return pd.Series(dtype="float64")

    expenses = df.groupby("category")["amount"].sum()

    return expenses


def get_monthly_spending():
    """Calculate total spending for each month."""

    df = load_transactions()

    if df.empty:
        return pd.Series(dtype="float64")

    # Convert date to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remove rows with invalid dates
    df = df.dropna(subset=["date"])

    # Extract Year-Month
    df["month"] = df["date"].dt.to_period("M")

    # Calculate monthly expenses
    monthly_expenses = df.groupby("month")["amount"].sum()

    return monthly_expenses


# Test monthly spending
print(get_monthly_spending())
from calendar import month_name
from datetime import date

import pandas as pd

from . import database


def load_transactions_df():
    rows = database.fetch_all_transactions()
    df = pd.DataFrame(
        rows, columns=["id", "date", "type", "category", "description", "amount"]
    )
    if df.empty:
        return df
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    return df


def month_summary(df, year, month):
    if df.empty:
        return 0.0, 0.0, 0.0
    scoped = df[(df["year"] == year) & (df["month"] == month)]
    income = float(scoped.loc[scoped["type"] == "income", "amount"].sum())
    expense = float(scoped.loc[scoped["type"] == "expense", "amount"].sum())
    return income, expense, income - expense


def category_breakdown(df, year, month):
    if df.empty:
        return pd.Series(dtype=float)
    scoped = df[(df["year"] == year) & (df["month"] == month) & (df["type"] == "expense")]
    if scoped.empty:
        return pd.Series(dtype=float)
    return scoped.groupby("category")["amount"].sum().sort_values(ascending=False)


def budget_status(df, budgets, year, month):
    spent = category_breakdown(df, year, month)
    categories = sorted(set(budgets.keys()) | set(spent.index))
    records = []
    for cat in categories:
        limit = float(budgets.get(cat, 0.0))
        used = float(spent.get(cat, 0.0))
        pct = (used / limit * 100) if limit > 0 else (100.0 if used > 0 else 0.0)
        records.append(
            {
                "category": cat,
                "spent": used,
                "limit": limit,
                "remaining": limit - used,
                "pct_used": pct,
            }
        )
    out = pd.DataFrame(records)
    if not out.empty:
        out = out.sort_values("pct_used", ascending=False).reset_index(drop=True)
    return out


def monthly_trend(df, months=6, end_year=None, end_month=None):
    today = date.today()
    end_year = end_year or today.year
    end_month = end_month or today.month

    periods = []
    y, m = end_year, end_month
    for _ in range(months):
        periods.append((y, m))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    periods.reverse()

    records = []
    for y, m in periods:
        income, expense, net = month_summary(df, y, m)
        records.append(
            {
                "label": f"{month_name[m][:3]} {str(y)[-2:]}",
                "year": y,
                "month": m,
                "income": income,
                "expense": expense,
                "net": net,
            }
        )
    return pd.DataFrame(records)


def savings_rate(income, expense):
    if income <= 0:
        return 0.0
    return max(0.0, (income - expense) / income * 100)

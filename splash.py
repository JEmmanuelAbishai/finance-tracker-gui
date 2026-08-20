from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, StringVar, Toplevel

from customtkinter import CTkSlider, CTkEntry
from CTkMessagebox import CTkMessagebox

from transactions import add_transaction, reset_transactions
from visual import plot_expense_by_category, plot_monthly_spending
from transactions_log import log_transaction, reset_transaction_log

import csv
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sys
import os


#Configuration for assets and output paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

budget = 0


def relative_to_assets(path: str) -> Path:
    """Return the absolute path to an asset file."""
    return ASSETS_PATH / Path(path)


#Add Window
window = Tk()
window.geometry("1000x550")
window.configure(bg="#FFFFFF")
window.title("Finance Tracker")
window.resizable(False, False)


canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=550,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)


# -------------------------------------------------------------------
# Budget Slider
# -------------------------------------------------------------------

slider_value_var = StringVar()
slider_value_var.set("Amount: 0")

slider = CTkSlider(
    window,
    from_=0,
    to=100000,
    number_of_steps=100,
    width=300
)
slider.place(x=350, y=300)


slider_value_label = canvas.create_text(
    500.0,
    335.0,
    anchor="center",
    text=slider_value_var.get(),
    fill="#FFFFFF",
    font=("Barlow", 14, "-1")
)


def on_slider_change(value):
    """Update the budget whenever the slider is moved."""

    global budget

    budget = int(float(value))

    slider_value_var.set(f"Amount: {budget}")

    canvas.itemconfig(
        slider_value_label,
        text=slider_value_var.get()
    )


slider.configure(command=on_slider_change)

# Initialize budget
budget = int(slider.get())


#Add Transaction
def handle_add_transaction():
    """Validate and add a new transaction."""

    global budget

    date = entry_3.get()
    category = entry_2.get()
    amount = entry_1.get()

    try:
        from proc import load_transactions

        # Validate input
        if not date or not category or not amount:
            CTkMessagebox(
                title="Input Error",
                message="Please fill in all fields.",
                icon="warning"
            )
            return

        # Validate amount
        try:
            float_amount = float(amount)
        except ValueError:
            CTkMessagebox(
                title="Input Error",
                message="Amount must be a number.",
                icon="warning"
            )
            return

        # Load existing transactions
        df = load_transactions()

        if not df.empty and "amount" in df.columns:
            df["amount"] = pd.to_numeric(
                df["amount"],
                errors="coerce"
            )

            total_expenses = df["amount"].sum()
        else:
            total_expenses = 0

        # Check budget
        current_budget = int(float(slider.get()))

        if total_expenses + float_amount > current_budget:
            CTkMessagebox(
                title="Insufficient Budget",
                message="Insufficient budget.",
                icon="warning"
            )
            return

        # Add transaction
        add_transaction(
            date,
            category,
            float_amount
        )

        # Log transaction
        log_transaction(
            date,
            category,
            float_amount
        )

        # Clear input fields
        entry_3.delete(0, "end")
        entry_2.delete(0, "end")
        entry_1.delete(0, "end")

        CTkMessagebox(
            title="Success",
            message="Transaction added successfully!",
            icon="check"
        )

    except Exception as e:
        CTkMessagebox(
            title="Error",
            message=f"Error adding transaction: {e}",
            icon="cancel"
        )


#Reset Transactions
def handle_reset_transactions():
    """Delete all transaction records after confirmation."""

    confirm = CTkMessagebox(
        title="Reset Data",
        message="Are you sure you want to delete all transactions?",
        icon="warning",
        option_1="Yes",
        option_2="No"
    )

    if confirm.get() == "Yes":
        reset_transactions()
        reset_transaction_log()

        CTkMessagebox(
            title="Reset",
            message="All transactions have been deleted.",
            icon="check"
        )


    #Expense Chart
def show_expense_chart_in_gui():
    """Display expense data in a chart."""

    from proc import load_transactions

    df = load_transactions()

    # Check whether transactions exist
    if df.empty or "amount" not in df.columns:
        CTkMessagebox(
            title="No Data",
            message="No transactions available.",
            icon="warning"
        )
        return

    # Convert amounts to numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Remove rows with invalid amounts
    df = df.dropna(subset=["amount"])

    if df.empty:
        CTkMessagebox(
            title="No Data",
            message="No valid transactions to plot.",
            icon="warning"
        )
        return

    # Group expenses by category
    expenses = df.groupby("category")["amount"].sum()

    if expenses.empty or expenses.sum() == 0:
        CTkMessagebox(
            title="No Data",
            message="No expense data available.",
            icon="warning"
        )
        return

    # Create chart
    fig, ax = plt.subplots(figsize=(6, 4))

    expenses.plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90,
        ax=ax
    )

    ax.set_title("Spending by Category")
    ax.set_ylabel("")

    # Display chart in a new window
    chart_window = Toplevel(window)
    chart_window.title("Expense Chart")
    chart_window.geometry("700x500")

    chart_canvas = FigureCanvasTkAgg(
        fig,
        master=chart_window
    )

    chart_canvas.draw()
    chart_canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )


    #Login GUI
def show_login_gui():
    """Display the login window."""

    login_win = Toplevel(window)

    login_win.title("RSPLASH")
    login_win.geometry("1000x550")
    login_win.configure(bg="#FFFFFF")
    login_win.resizable(False, False)
    login_win.grab_set()

    # Set icon if available
    try:
        login_win.iconbitmap(icon_path)
    except Exception:
        pass

    login_canvas = Canvas(
        login_win,
        bg="#FFFFFF",
        height=550,
        width=1000,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    login_canvas.place(x=0, y=0)

    # Load login images
    try:
        login_win.login_image_1 = PhotoImage(
            file=relative_to_assets("frame_w.png")
        )

        login_win.login_image_2 = PhotoImage(
            file=relative_to_assets("frame_b.png")
        )

        login_canvas.create_image(
            500.0,
            275.0,
            image=login_win.login_image_1
        )

        login_canvas.create_image(
            501.0,
            274.0,
            image=login_win.login_image_2
        )

    except Exception:
        pass

    #Login Functionality
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "password":
            login_win.destroy()
            window.deiconify()

        else:
            CTkMessagebox(
                title="Login Failed",
                message="Invalid credentials!",
                icon="cancel"
            )

    #Username Entry
    username_entry = CTkEntry(
        login_win,
        width=300,
        placeholder_text="Username"
    )

    username_entry.place(
        x=350,
        y=280
    )

    #Password Entry
    password_entry = CTkEntry(
        login_win,
        width=300,
        placeholder_text="Password",
        show="*"
    )

    password_entry.place(
        x=350,
        y=340
    )

    #Login Button with Fallback
    try:
        login_button_image = PhotoImage(
            file=relative_to_assets("button_login.png")
        )

        login_btn = Button(
            login_win,
            image=login_button_image,
            borderwidth=0,
            highlightthickness=0,
            command=attempt_login,
            relief="flat"
        )

        login_btn.image = login_button_image

    except Exception:
        login_btn = Button(
            login_win,
            text="Login",
            command=attempt_login,
            relief="flat"
        )

    login_btn.place(
        x=350.0,
        y=416.0,
        width=300.0,
        height=55.0
    )

    # Hide the main window until login succeeds
    window.withdraw()

    login_win.protocol(
        "WM_DELETE_WINDOW",
        window.destroy
    )


#Start Application

show_login_gui()

window.mainloop()
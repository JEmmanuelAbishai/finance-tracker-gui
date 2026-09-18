import os
import sys
import tkinter.font as tkfont

APP_NAME = "Ripple"
APP_MIN_SIZE = (1000, 600)


def get_base_dir():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_dir():
    if getattr(sys, "frozen", False):
        base = os.path.join(os.environ["LOCALAPPDATA"], APP_NAME)
    else:
        base = os.path.join(get_base_dir(), "data")
    os.makedirs(base, exist_ok=True)
    return base


BASE_DIR = get_base_dir()
DATA_DIR = get_data_dir()
DB_PATH = os.path.join(DATA_DIR, "finance_tracker.db")


def _first_available_font(candidates):
    try:
        available = set(tkfont.families())
    except Exception:
        return candidates[-1]
    for name in candidates:
        if name in available:
            return name
    return candidates[-1]



UI_FONT = "TkDefaultFont"
MONO_FONT = "TkFixedFont"

FONTS = {
    "h1": (UI_FONT, 25, "bold"),
    "h2": (UI_FONT, 18, "bold"),
    "h3": (UI_FONT, 14, "bold"),
    "body": (UI_FONT, 13, "normal"),
    "small": (UI_FONT, 11, "normal"),
    "nav": (UI_FONT, 13, "normal"),
    "figure": (MONO_FONT, 22, "bold"),
    "mono": (MONO_FONT, 13, "normal"),
}


def init_fonts():

    global UI_FONT, MONO_FONT

    UI_FONT = _first_available_font(
        ["JetBrains Mono", "Segoe UI", "Helvetica Neue", "Ubuntu", "Arial", "TkDefaultFont"]
    )
    MONO_FONT = _first_available_font(
        ["JetBrains Mono", "Consolas", "SF Mono", "Ubuntu Mono", "Courier New", "TkFixedFont"]
    )

    FONTS.clear()
    FONTS.update({
        "h1": (UI_FONT, 25, "bold"),
        "h2": (UI_FONT, 18, "bold"),
        "h3": (UI_FONT, 14, "bold"),
        "body": (UI_FONT, 13, "normal"),
        "small": (UI_FONT, 11, "normal"),
        "nav": (UI_FONT, 13, "normal"),
        "figure": (MONO_FONT, 22, "bold"),
        "mono": (MONO_FONT, 13, "normal"),
    })


PALETTE = {
    "dark": {
        "bg": "#15191C",
        "surface": "#1E2327",
        "surface_alt": "#262D32",
        "border": "#333C42",
        "text": "#F3F1EB",
        "text_muted": "#8E9AA3",
        "accent": "#5E86C2",
        "accent_hover": "#89A0C2",
        "amber": "#E3A23D",
        "coral": "#E2685A",
        "blue": "#5B9BD9",
    },
    "light": {
        "bg": "#EEF1F3",
        "surface": "#FFFFFF",
        "surface_alt": "#F3F5F7",
        "border": "#DCE1E5",
        "text": "#1B2226",
        "text_muted": "#5B6670",
        "accent": "#1E9E7E",
        "accent_hover": "#187F65",
        "amber": "#C9821A",
        "coral": "#D14E3C",
        "blue": "#3E7CB1",
    },
}

# Categories
EXPENSE_CATEGORIES = [
    "Housing",
    "Food & Dining",
    "Transportation",
    "Utilities",
    "Entertainment",
    "Health & Fitness",
    "Shopping",
    "Personal Care",
    "Education",
    "Other",
]

INCOME_CATEGORIES = ["Salary", "Freelance", "Investments", "Gifts", "Other"]

DEFAULT_BUDGETS = {
    "Housing": 1200.0,
    "Food & Dining": 600.0,
    "Transportation": 250.0,
    "Utilities": 200.0,
    "Entertainment": 150.0,
    "Health & Fitness": 120.0,
    "Shopping": 200.0,
    "Personal Care": 80.0,
    "Education": 0.0,
    "Other": 100.0,
}
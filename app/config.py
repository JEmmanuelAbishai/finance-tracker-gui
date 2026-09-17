import os
import tkinter.font as tkfont

APP_NAME = "Splash"
APP_MIN_SIZE = (1180, 720)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
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
    """
    Re-resolve UI_FONT / MONO_FONT now that a Tk root exists, preferring
    JetBrains Mono (registered via app.fonts.load_custom_fonts()) for
    both the UI and mono roles, and rebuild FONTS IN PLACE so any module
    that already did `from app.config import FONTS` still sees the update.
    """
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
        "accent": "#2C1092",
        "accent_hover": "#249C7E",
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
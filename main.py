import os

import customtkinter as ctk

from app import config, database
from app.fonts import load_custom_fonts
from app.ui.app_window import AppWindow
from app.ui.login import LoginView


def get_icon_path():
    base = config.get_base_dir()
    return os.path.join(base, "app", "assets", "icon.ico")


class RippleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        load_custom_fonts()
        config.init_fonts()

        self.title(config.APP_NAME)
        self.geometry(f"{config.APP_MIN_SIZE[0]}x{config.APP_MIN_SIZE[1]}")
        self.minsize(*config.APP_MIN_SIZE)
        self.maxsize(*config.APP_MIN_SIZE)
        self.resizable(False, False)

        icon_path = get_icon_path()
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
        else:
            print(f"[icon] Warning: icon not found at {icon_path}")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        database.init_db()

        self.current_frame = None
        self._show_login()

    def _clear(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    @staticmethod
    def _theme_for_current_mode():
        mode = ctk.get_appearance_mode().lower()
        return mode if mode in config.PALETTE else "dark"

    def _show_login(self):
        self._clear()
        theme = config.PALETTE[self._theme_for_current_mode()]
        self.current_frame = LoginView(self, theme, on_success=self._show_app)

    def _show_app(self, _username):
        self._clear()
        self.current_frame = AppWindow(
            self, self._theme_for_current_mode(),
            on_logout=self._show_login, on_appearance_change=self._on_appearance_change,
        )

    def _on_appearance_change(self, mode):
        self._clear()
        self.current_frame = AppWindow(
            self, mode, on_logout=self._show_login, on_appearance_change=self._on_appearance_change,
        )


def main():
    app = RippleApp()
    app.mainloop()


if __name__ == "__main__":
    main()
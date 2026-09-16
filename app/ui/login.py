import customtkinter as ctk

from .. import config, database


class LoginView(ctk.CTkFrame):
    def __init__(self, master, theme, on_success):
        super().__init__(master, fg_color=theme["bg"])
        self.theme = theme
        self.on_success = on_success
        self.mode = "login" if database.has_any_user() else "register"
        self.pack(fill="both", expand=True)
        self._build()

    def _build(self):
        theme = self.theme
        card = ctk.CTkFrame(self, width=380, corner_radius=16, fg_color=theme["surface"])
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card, text=config.APP_NAME, font=config.FONTS["h1"], text_color=theme["accent"]
        ).grid(row=0, column=0, pady=(38, 2), padx=40)

        self.subtitle = ctk.CTkLabel(
            card,
            text="Create your account" if self.mode == "register" else "Welcome back",
            font=config.FONTS["body"], text_color=theme["text_muted"],
        )
        self.subtitle.grid(row=1, column=0, pady=(0, 24))

        self.username = ctk.CTkEntry(card, placeholder_text="Username", width=280, height=40)
        self.username.grid(row=2, column=0, padx=40, pady=6)

        self.password = ctk.CTkEntry(
            card, placeholder_text="Password", show="\u2022", width=280, height=40
        )
        self.password.grid(row=3, column=0, padx=40, pady=6)
        self.password.bind("<Return>", lambda _e: self._submit())
        self.username.bind("<Return>", lambda _e: self.password.focus())

        self.error = ctk.CTkLabel(card, text="", text_color=theme["coral"], font=config.FONTS["small"])
        self.error.grid(row=4, column=0, pady=(4, 0))

        self.submit_btn = ctk.CTkButton(
            card,
            text="Create account" if self.mode == "register" else "Log in",
            command=self._submit, fg_color=theme["accent"], hover_color=theme["accent_hover"],
            height=40, width=280,
        )
        self.submit_btn.grid(row=5, column=0, pady=(18, 8), padx=40)

        self.toggle_btn = ctk.CTkButton(
            card,
            text="Already have an account? Log in"
            if self.mode == "register" else "New here? Create an account",
            command=self._toggle_mode, fg_color="transparent", hover_color=theme["surface_alt"],
            text_color=theme["text_muted"], height=30, width=280,
        )
        self.toggle_btn.grid(row=6, column=0, pady=(0, 30), padx=40)

        self.username.focus()

    def _toggle_mode(self):
        self.mode = "register" if self.mode == "login" else "login"
        self.error.configure(text="")
        self.subtitle.configure(
            text="Create your account" if self.mode == "register" else "Welcome back"
        )
        self.submit_btn.configure(text="Create account" if self.mode == "register" else "Log in")
        self.toggle_btn.configure(
            text="Already have an account? Log in"
            if self.mode == "register" else "New here? Create an account"
        )

    def _submit(self):
        username = self.username.get().strip()
        password = self.password.get()
        if not username or not password:
            self.error.configure(text="Enter a username and password.")
            return
        try:
            if self.mode == "register":
                if len(password) < 4:
                    self.error.configure(text="Password should be at least 4 characters.")
                    return
                database.create_user(username, password)
                self.on_success(username)
            else:
                if database.verify_user(username, password):
                    self.on_success(username)
                else:
                    self.error.configure(text="Incorrect username or password.")
        except ValueError as exc:
            self.error.configure(text=str(exc))

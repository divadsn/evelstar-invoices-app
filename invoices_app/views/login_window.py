import os

import customtkinter as ctk
from pathlib import Path
from tkinter import messagebox

from PIL import Image, ImageTk
from async_tkinter_loop import async_mainloop, async_handler
from async_tkinter_loop.mixins import AsyncCTk
from customtkinter import CTkImage

from invoices_app.api import FirebaseException, FirebaseAuthClient
from invoices_app.api.firebase import extract_firebase_config


class LoginWindow(ctk.CTk, AsyncCTk):
    def __init__(self):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        super().__init__()
        self.title("Zaloguj się")
        self.resizable(False, False)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(padx=20, pady=5)

        # Logo
        images_dir = Path(__file__).parent / ".." / "images"
        logo = CTkImage(light_image=Image.open(images_dir / "logo.png"), dark_image=Image.open(images_dir / "logo_white.png"), size=(200, 82))
        logo_label = ctk.CTkLabel(frame, image=logo, text="")
        logo_label.image = logo
        logo_label.pack(pady=20)

        input_frame = ctk.CTkFrame(frame, fg_color="transparent")
        input_frame.pack()

        # Email entry
        ctk.CTkLabel(input_frame, text="E-Mail:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = ctk.CTkEntry(input_frame, width=180)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)

        # Password entry
        ctk.CTkLabel(input_frame, text="Hasło:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ctk.CTkEntry(input_frame, width=180, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Login button
        self.login_button = ctk.CTkButton(frame, text="Zaloguj się", height=32, command=self.login)
        self.login_button.pack(padx=5, pady=20, fill="x")

        # Center the window (after all widgets are added)
        self.eval("tk::PlaceWindow . center")

    @async_handler
    async def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione")
            return

        # Disable the login button
        self.login_button.configure(state="disabled")

        # Get Firebase config
        firebase_config = await extract_firebase_config()
        auth_client = FirebaseAuthClient(firebase_config["apiKey"], firebase_config["appId"])

        try:
            await auth_client.login(email, password)
        except FirebaseException:
            self.login_button.configure(state="normal")
            messagebox.showerror("Błąd", "Logowanie nie powiodło się. Sprawdź email i hasło, a następnie spróbuj jeszcze raz.")
            return

        messagebox.showinfo("Sukces", "Zalogowano pomyślnie")

        # Close the window
        self.destroy()


if __name__ == "__main__":
    login_window = LoginWindow()
    login_window.async_mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os


def check_login_status():
    # Dummy function to check if the user is logged in
    return False  # Change this based on actual authentication logic


def login():
    email = email_entry.get()
    password = password_entry.get()

    # Dummy authentication logic
    if email == "admin@example.com" and password == "password":
        show_invoices_window()
    else:
        messagebox.showerror("Błąd", "Niepoprawny email lub hasło")


def show_login_window():
    global email_entry, password_entry

    root = tk.Tk()
    root.title("Login")
    root.geometry("400x300")

    frame = tk.Frame(root)
    frame.pack(pady=20)

    try:
        image = Image.open("invoices_app/images/logo.png")
        logo = ImageTk.PhotoImage(image)
        logo_label = tk.Label(frame, image=logo)
        logo_label.image = logo
        logo_label.pack()
    except Exception as e:
        print(f"Error loading logo: {e}")

    tk.Label(frame, text="Zaloguj się").pack(pady=10)

    input_frame = tk.Frame(frame)
    input_frame.pack()

    tk.Label(input_frame, text="E-Mail:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    email_entry = tk.Entry(input_frame)
    email_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(input_frame, text="Hasło:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    password_entry = tk.Entry(input_frame, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(frame, text="Zaloguj", command=login).pack(pady=20)

    root.mainloop()


def show_invoices_window():
    root = tk.Tk()
    root.title("Faktury")
    root.geometry("800x400")

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    invoices_menu = tk.Menu(menu_bar, tearoff=0)
    invoices_menu.add_command(label="Dodaj fakturę")
    menu_bar.add_cascade(label="Opcje", menu=invoices_menu)

    columns = ("Numer faktury", "Sprzedawca", "Data", "Brutto", "VAT", "Netto", "Status", "Wysłano")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    root.mainloop()


if check_login_status():
    show_invoices_window()
else:
    show_login_window()

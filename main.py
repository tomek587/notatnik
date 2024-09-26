import tkinter as tk
from tkinter import ttk, messagebox
from baza import Database

baza = Database(host="localhost", user="root", password="", database="notatnik")
baza.create_tables()


def logowanie():
    if True:
        otworz_notatnik()


def otworz_notatnik():
    login_frame.destroy()
    root.geometry("600x615")

    notatnik_frame = tk.Frame(root)
    notatnik_frame.pack(pady=20)

    tk.Label(notatnik_frame, text=f"Witaj, login użytkownika", font=("Helvetica", 14)).pack(pady=10)

    notatka_entry = tk.Text(notatnik_frame, height=10, width=40)
    notatka_entry.pack(padx=10, pady=10)

    dodaj_btn = ttk.Button(notatnik_frame, text="Dodaj notatkę")
    dodaj_btn.pack(padx=10, pady=5)

    usun_notatke_btn = ttk.Button(notatnik_frame, text="Usuń notatkę")
    usun_notatke_btn.pack(padx=10, pady=5)

    notatki_listbox = tk.Listbox(notatnik_frame, height=10, width=50)
    notatki_listbox.pack(padx=10, pady=10)

    notatki_listbox.bind('<<ListboxSelect>>')

    wyloguj_btn = ttk.Button(notatnik_frame, text="Wyloguj", command=lambda: wyloguj(notatnik_frame))
    wyloguj_btn.pack(pady=10)


def wyloguj(notatnik_frame):
    notatnik_frame.destroy()
    zaladuj_okno_logowania()


def zaladuj_okno_logowania():
    global login_frame
    root.geometry("300x150")

    login_frame = tk.Frame(root)
    login_frame.pack(pady=20)

    login_label = ttk.Label(login_frame, text="Login:")
    login_label.grid(row=0, column=0, padx=10, pady=5)

    global login_entry
    login_entry = ttk.Entry(login_frame)
    login_entry.grid(row=0, column=1, padx=10, pady=5)

    haslo_label = ttk.Label(login_frame, text="Hasło:")
    haslo_label.grid(row=1, column=0, padx=10, pady=5)

    global haslo_entry
    haslo_entry = ttk.Entry(login_frame, show="*")
    haslo_entry.grid(row=1, column=1, padx=10, pady=5)

    logowanie_btn = ttk.Button(login_frame, text="Zaloguj", command=logowanie)
    logowanie_btn.grid(row=2, column=0, padx=10, pady=10)

    rejestracja_btn = ttk.Button(login_frame, text="Zarejestruj")
    rejestracja_btn.grid(row=2, column=1, padx=10, pady=10)


root = tk.Tk()
root.title("Notatnik")
root.iconbitmap("icon.ico")

zaladuj_okno_logowania()

root.mainloop()

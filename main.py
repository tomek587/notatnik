import tkinter as tk
from tkinter import ttk, messagebox
from baza import Database

baza = Database(host="localhost", user="root", password="", database="notatnik")

baza.create_tables()


# dsdsd
def rejestracja():
    login = login_entry.get().strip()
    password = haslo_entry.get().strip()

    if login and password:
        if baza.check_user(login, password):
            messagebox.showerror("Taki użytkownik już istnieje")
        else:
            baza.insert_user(login, password)
            messagebox.showinfo("Rejestracja udana")
    else:
        messagebox.showerror("Podaj login i hasło")


def logowanie():
    login = login_entry.get().strip()
    password = haslo_entry.get().strip()

    user = baza.check_user(login, password)

    if user:
        messagebox.showinfo(f"Zalogowano jako {login}")
        otworz_notatnik(login)
    else:
        messagebox.showerror("Błędny login lub hasło")


def otworz_notatnik(login):
    login_frame.destroy()

    notatnik_frame = tk.Frame(root)
    notatnik_frame.pack(pady=20)

    tk.Label(notatnik_frame, text=f"Witaj, {login}", font=("Helvetica", 14)).pack(pady=10)

    notatka_entry = tk.Text(notatnik_frame, height=5, width=40)
    notatka_entry.pack(padx=10, pady=10)

    dodaj_btn = ttk.Button(notatnik_frame, text="Dodaj notatkę", command=lambda: dodaj_notatke(notatka_entry, login))
    dodaj_btn.pack(padx=10, pady=10)

    notatki_listbox = tk.Listbox(notatnik_frame, height=10, width=50)
    notatki_listbox.pack(padx=10, pady=10)

    odswiez_btn = ttk.Button(notatnik_frame, text="Odśwież notatki", command=lambda: wyswietl_notatki(notatki_listbox,
                                                                                                      login))
    odswiez_btn.pack(padx=10, pady=10)

    wyswietl_notatki(notatki_listbox, login)


def dodaj_notatke(notatka_entry, login):
    text = notatka_entry.get("1.0", tk.END).strip()
    if text:
        user_id = baza.get_user_id(login)
        baza.insert_notatka(text, user_id)
        notatka_entry.delete("1.0", tk.END)
    else:
        messagebox.showerror("Notatka nie może być pasta")


def wyswietl_notatki(notatki_listbox, login):
    notatki_listbox.delete(0, tk.END)
    user_id = baza.get_user_id(login)
    notatki = baza.select_notatki_by_user(user_id)

    if notatki:
        for notatka in notatki:
            notatki_listbox.insert(tk.END, notatka[1])
    else:
        notatki_listbox.insert(tk.END, "Brak notatek")


# Aplikacja
root = tk.Tk()
root.title("Logowanie i Rejestracja")
root.geometry("400x300")

login_frame = tk.Frame(root)
login_frame.pack(pady=20)

login_label = ttk.Label(login_frame, text="Login:")
login_label.grid(row=0, column=0, padx=10, pady=5)

login_entry = ttk.Entry(login_frame)
login_entry.grid(row=0, column=1, padx=10, pady=5)

haslo_label = ttk.Label(login_frame, text="Hasło:")
haslo_label.grid(row=1, column=0, padx=10, pady=5)

haslo_entry = ttk.Entry(login_frame, show="*")
haslo_entry.grid(row=1, column=1, padx=10, pady=5)

logowanie_btn = ttk.Button(login_frame, text="Zaloguj", command=logowanie)
logowanie_btn.grid(row=2, column=0, padx=10, pady=10)

rejestracja_btn = ttk.Button(login_frame, text="Zarejestruj", command=rejestracja)
rejestracja_btn.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from baza import Database

baza = Database(host="localhost", user="root", password="", database="notatnik")
baza.create_tables()


def rejestracja():
    login = login_entry.get().strip()
    password = haslo_entry.get().strip()

    if login and password:
        if baza.check_user(login, password):
            messagebox.showerror(title="Error", message="Taki użytkownik już istnieje")
        else:
            baza.insert_user(login, password)
            otworz_notatnik(login)
    else:
        messagebox.showerror(title="Error", message="Podaj login i hasło")


def logowanie():
    login = login_entry.get().strip()
    password = haslo_entry.get().strip()

    user = baza.check_user(login, password)

    if user:
        otworz_notatnik(login)
    else:
        messagebox.showerror(title="Error", message="Błędny login lub hasło")


def otworz_notatnik(login):
    login_frame.destroy()
    root.geometry("800x600")

    notatnik_frame = tk.Frame(root, bg="#2F2F2F")
    notatnik_frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(notatnik_frame, text=f"Witaj, {login}", font=("Helvetica", 14), bg="#2F2F2F",
             fg="white").grid(row=0,
                              column=0,
                              columnspan=3,
                              pady=10)

    notatka_entry = tk.Text(notatnik_frame, height=10, width=40, bg="#4F4F4F", fg="white", insertbackground="white")
    notatka_entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2)

    wyszukaj_label = tk.Label(notatnik_frame, text="Wyszukaj notatkę:", bg="#2F2F2F", fg="white")
    wyszukaj_label.grid(row=0, column=2, padx=10)

    wyszukaj_entry = ttk.Entry(notatnik_frame)
    wyszukaj_entry.grid(row=0, column=3, padx=10)

    wyszukaj_btn = ttk.Button(notatnik_frame, text="Szukaj", command=lambda: wyszukaj_notatke(wyszukaj_entry,
                                                                                              login, notatki_listbox))
    wyszukaj_btn.grid(row=0, column=4, padx=10)

    photo_add = tk.PhotoImage(file=r"image/add_btn.jpg")
    dodaj_btn = tk.Button(notatnik_frame, text="Dodaj notatkę", image=photo_add, bg="#5CB85C", fg="white",
                          command=lambda: dodaj_notatke(notatka_entry, login, notatki_listbox))
    dodaj_btn.grid(row=2, column=0, padx=10, pady=5)

    photo_delete = tk.PhotoImage(file=r"image/delete_btn.jpg")
    usun_notatke_btn = tk.Button(notatnik_frame, text="Usuń notatkę", image=photo_delete, bg="#D9534F", fg="white",
                                 command=lambda: usun_wybrana_notatka(notatki_listbox, notatka_entry, login))
    usun_notatke_btn.grid(row=2, column=1, padx=10, pady=5)

    notatki_listbox = tk.Listbox(notatnik_frame, height=15, width=50, bg="#4F4F4F", fg="white",
                                 selectbackground="#6C757D", selectforeground="white")
    notatki_listbox.grid(row=1, column=3, rowspan=2, padx=10, pady=10)

    notatki_listbox.bind('<<ListboxSelect>>',
                         lambda event: wyswietl_zaznaczona_notatka(notatki_listbox, notatka_entry, login))

    photo_logout = tk.PhotoImage(file=r"image/logout_btn.jpg")
    wyloguj_btn = ttk.Button(notatnik_frame, text="Wyloguj", image=photo_logout,
                             command=lambda: wyloguj(notatnik_frame))
    wyloguj_btn.grid(row=3, column=0, pady=10)

    wyswietl_notatki(notatki_listbox, login)


def dodaj_notatke(notatka_entry, login, notatki_listbox):
    text = notatka_entry.get("1.0", tk.END).strip()
    if text:
        user_id = baza.get_user_id(login)
        baza.insert_notatka(text, user_id)
        notatka_entry.delete("1.0", tk.END)
        wyswietl_notatki(notatki_listbox, login)
    else:
        messagebox.showerror(title="Error", message="Notatka nie może być pusta")


def wyswietl_notatki(notatki_listbox, login):
    notatki_listbox.delete(0, tk.END)
    user_id = baza.get_user_id(login)
    notatki = baza.select_notatki_by_user(user_id)

    if not notatki:
        notatki_listbox.insert(tk.END, "Brak notatek")
    else:
        for notatka in notatki:
            short_text = (notatka[1][:41] + '...') if len(notatka[1]) > 30 else notatka[1]
            timestamp = notatka[3].strftime('%d-%m-%Y')
            notatki_listbox.insert(tk.END, f"{short_text}  {timestamp}")


def wyswietl_zaznaczona_notatka(notatki_listbox, notatka_entry, login):
    selected_index = notatki_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        user_id = baza.get_user_id(login)
        notatki = baza.select_notatki_by_user(user_id)
        if selected_index < len(notatki):
            notatka_entry.delete("1.0", tk.END)
            notatka_entry.insert(tk.END, notatki[selected_index][1])


def usun_wybrana_notatka(notatki_listbox, notatka_entry, login):
    selected_index = notatki_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        user_id = baza.get_user_id(login)
        notatki = baza.select_notatki_by_user(user_id)
        if selected_index < len(notatki):
            notatka_id = notatki[selected_index][0]
            baza.delete_notatka(notatka_id)
            notatka_entry.delete("1.0", tk.END)
            wyswietl_notatki(notatki_listbox, login)


def wyloguj(notatnik_frame):
    notatnik_frame.destroy()
    zaladuj_okno_logowania()


def zaladuj_okno_logowania():
    global login_frame
    root.geometry("300x150")
    root.configure(bg="#2F2F2F")

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

    rejestracja_btn = ttk.Button(login_frame, text="Zarejestruj", command=rejestracja)
    rejestracja_btn.grid(row=2, column=1, padx=10, pady=10)


root = tk.Tk()
root.title("Notatnik")
root.configure(bg="#2F2F2F")
root.iconbitmap("image/icon.ico")

zaladuj_okno_logowania()

root.mainloop()

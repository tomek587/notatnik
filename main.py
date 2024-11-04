import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from baza import Database
import configparser


config = configparser.ConfigParser()
config.read("config.ini")

host = config["baza"]["host"]
user = config["baza"]["user"]
password = config["baza"]["password"]
database = config["baza"]["dbname"]

baza = Database(host=host, user=user, password=password, database=database)
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
    root.geometry("700x350")
    root.configure(bg="#2E2E2E")

    notatnik_frame = tk.Frame(root, bg="#2E2E2E")
    notatnik_frame.pack(pady=20)

    top_frame = tk.Frame(notatnik_frame, bg="#2E2E2E")
    top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

    tk.Label(top_frame, text=f"Witaj, {login}", font=("Helvetica", 14), bg="#2E2E2E", fg="white").pack(side=tk.LEFT, padx=10)

    wyloguj_btn = ttk.Button(top_frame, text="Wyloguj", command=lambda: wyloguj(notatnik_frame), style="TButton")
    wyloguj_btn.pack(side=tk.LEFT, padx=10)

    search_frame = tk.Frame(top_frame, bg="#2E2E2E")
    search_frame.pack(side=tk.RIGHT, padx=10)

    search_entry = tk.Entry(search_frame, width=20, bg="#444444", fg="white", insertbackground='white',)
    search_entry.pack(side=tk.LEFT, padx=5)

    search_btn = ttk.Button(search_frame, text="Szukaj", command=lambda: wyswietl_notatki(notatki_listbox, login,
                                                                                          search_entry.get()))
    search_btn.pack(side=tk.LEFT)

    left_frame = tk.Frame(notatnik_frame, bg="#2E2E2E")
    left_frame.pack(side=tk.LEFT, padx=10)

    notatka_entry = tk.Text(left_frame, height=10, width=30, bg="#444444", fg="white", insertbackground='white')
    notatka_entry.pack(padx=5, pady=5)

    button_frame = tk.Frame(left_frame, bg="#2E2E2E")
    button_frame.pack(pady=5)

    add_icon = Image.open("image/add_btn.png").resize((40, 40))
    add_icon = ImageTk.PhotoImage(add_icon)

    dodaj_btn = tk.Button(button_frame, image=add_icon, bg="#389654", fg="white",
                          command=lambda: dodaj_notatke(notatka_entry, login, notatki_listbox))
    dodaj_btn.image = add_icon
    dodaj_btn.pack(side=tk.LEFT, padx=5)

    delete_icon = Image.open("image/delete_btn.jpg").resize((40, 40))
    delete_icon = ImageTk.PhotoImage(delete_icon)

    usun_notatke_btn = tk.Button(button_frame, image=delete_icon, bg="#b83737", fg="white",
                                 command=lambda: usun_wybrana_notatka(notatki_listbox, notatka_entry, login))
    usun_notatke_btn.image = delete_icon
    usun_notatke_btn.pack(side=tk.LEFT, padx=5)

    right_frame = tk.Frame(notatnik_frame, bg="#2E2E2E")
    right_frame.pack(side=tk.LEFT, padx=10, anchor='n')

    notatki_listbox = tk.Listbox(right_frame, height=10, width=40, bg="#444444", fg="white", selectbackground="#555555")
    notatki_listbox.pack(padx=5, pady=5)

    notatki_listbox.bind('<<ListboxSelect>>',
                         lambda event: wyswietl_zaznaczona_notatka(notatki_listbox, notatka_entry, login))

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

def wyswietl_notatki(notatki_listbox, login, search_term=""):
    notatki_listbox.delete(0, tk.END)
    user_id = baza.get_user_id(login)
    notatki = baza.select_notatki_by_user(user_id)

    if not notatki:
        notatki_listbox.insert(tk.END, "Brak notatek")
    else:
        filtered_notatki = [notatka for notatka in notatki if search_term.lower() in notatka[1].lower()]

        if not filtered_notatki:
            notatki_listbox.insert(tk.END, "Brak wyników")
        else:
            for notatka in filtered_notatki:
                short_text = (notatka[1][:39] + '...') if len(notatka[1]) > 30 else notatka[1]
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
    root.configure(bg="#2E2E2E")

    login_frame = tk.Frame(root, bg="#2E2E2E")
    login_frame.pack(pady=20)

    login_label = ttk.Label(login_frame, text="Login:", style="TLabel")
    login_label.grid(row=0, column=0, padx=10, pady=5)

    global login_entry
    login_entry = ttk.Entry(login_frame)
    login_entry.grid(row=0, column=1, padx=10, pady=5)

    haslo_label = ttk.Label(login_frame, text="Hasło:", style="TLabel")
    haslo_label.grid(row=1, column=0, padx=10, pady=5)

    global haslo_entry
    haslo_entry = ttk.Entry(login_frame, show="*")
    haslo_entry.grid(row=1, column=1, padx=10, pady=5)

    logowanie_btn = ttk.Button(login_frame, text="Zaloguj", command=logowanie, style="TButton")
    logowanie_btn.grid(row=2, column=0, padx=10, pady=10)

    rejestracja_btn = ttk.Button(login_frame, text="Zarejestruj", command=rejestracja, style="TButton")
    rejestracja_btn.grid(row=2, column=1, padx=10, pady=10)

root = tk.Tk()
root.title("Notatnik")
root.iconbitmap("image/icon.ico")

style = ttk.Style()
style.configure("TLabel", background="#2E2E2E", foreground="white")

style.configure("TButton",
                background="#4E4E4E", foreground="white", padding=5)
style.map("TButton",
          background=[("active", "#6E6E6E"), ("pressed", "#5E5E5E")],
          foreground=[("active", "white"), ("pressed", "white")])

zaladuj_okno_logowania()

root.mainloop()

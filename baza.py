import mysql.connector
from mysql.connector import Error

host = 'localhost'
user = 'root'
password = ''
database = 'notatnik'


class Database:
    def __init__(self, host, user, password, database):
        try:
            connect = mysql.connector.connect(host=host, user=user, password=password)
            self.conn = connect
            self.cursor = self.conn.cursor()
            print("Połączono z serwerem MySQL.")

            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            print(f"Baza danych '{database}' została utworzona lub już istnieje.")

            self.conn.database = database
            print(f"Połączono z bazą danych '{database}'.")

            self.create_tables()

        except Error as e:
            print(f"Error: {e}")
            self.conn = None

    def create_tables(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    login VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)
            print("Tabela 'users' utworzona.")

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS notatki (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tresc TEXT NOT NULL,
                    user_id INT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            print("Tabela 'notatki' utworzona.")

            self.conn.commit()
            print("Tabele zostały utworzone poprawnie i zapisane w bazie danych.")
        except Error as e:
            print(f"Błąd przy tworzeniu tabel: {e}")

    def check_user(self, login, password):
        query = "SELECT * FROM users WHERE login = %s AND password = %s"
        self.cursor.execute(query, (login, password))
        user = self.cursor.fetchone()
        return user

    def insert_user(self, login, password):
        try:
            query = "INSERT INTO users (login, password) VALUES (%s, %s)"
            self.cursor.execute(query, (login, password))
            self.conn.commit()
        except mysql.connector.IntegrityError:
            return False
        return True

    def get_user_id(self, login):
        query = "SELECT id FROM users WHERE login = %s"
        self.cursor.execute(query, (login,))
        user_id = self.cursor.fetchone()
        return user_id[0] if user_id else None

    def insert_notatka(self, tresc, user_id):
        query = "INSERT INTO notatki (tresc, user_id) VALUES (%s, %s)"
        self.cursor.execute(query, (tresc, user_id))
        self.conn.commit()

    def select_notatki_by_user(self, user_id):
        query = "SELECT * FROM notatki WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        notatki = self.cursor.fetchall()
        return notatki

    def delete_last_notatka(self):
        query = "DELETE FROM notatki WHERE id = (SELECT MAX(id) FROM notatki)"
        self.cursor.execute(query)
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

db = Database(host, user, password, database)

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
            print(f"rood przy tworzeniu tabel: {e}")


db = Database(host, user, password, database)

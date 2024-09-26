import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self, host, user, password, database):
        try:
            connect = mysql.connector.connect(host=host, user=user, password=password)
            self.conn = connect
            self.cursor = self.conn.cursor()

            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            self.conn.commit()

            self.conn.database = database

            self.create_tables()

        except Error as e:
            print(f"Błąd przy tworzeniu bazy lub połączeniu: {e}")
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

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS notatki (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    tresc TEXT NOT NULL,
                    user_id INT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.conn.commit()

        except Error as e:
            print(f"Błąd przy tworzeniu tabel: {e}")
            self.conn = None

    def close(self):
        if self.conn:
            self.conn.close()

import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = sqlite3.connection.cursor()

    def crate_table(self):
        with self.connection:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                     id INT AUTO_INCREMENT PRIMARY KEY,
                      user_id INTEGER NOT NULL,
                      username TEXT
                )
            """)

    def add_user(self, user_id, username):
        with self.connection:
            self.cursor.execute("INSERT INTO user (user_id, username) VALUES(?, ?)",
            (user_id, username))

    

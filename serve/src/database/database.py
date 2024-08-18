import sqlite3
import configparser


class Database:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        database_path = config['SQLite3']['Path']

        self.database_connection = sqlite3.connect(database_path)

    def close(self):
        self.database_connection.close()

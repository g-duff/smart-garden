import sqlite3
import configparser

from .objects import Environment, Plant

class Database:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        database_path = config['SQLite3']['Path']

        self.connection = sqlite3.connect(database_path)

    def insert_environments(self, environments: list[Environment]):
        with self.connection:
            self.connection.executemany(f"""INSERT INTO environment 
                (timestamp, name, humidity, temperature) 
                VALUES (?, ?, ?, ?);""",
                ((e.timestamp, e.name, e.humidity, e.temperature) for e in environments)
                )

    def insert_plants(self, plants: list[Plant]):
        with self.connection:
            self.connection.executemany("""INSERT INTO plant 
                (name, timestamp, moisture_percent, moisture_voltage) 
                VALUES (?, ?, ?, ?);""",
                ((p.name, p.timestamp, p.moisture_percent, p.moisture_voltage) for p in plants),
                )

    def select_environments(self, names: list[str], from_date: str, to_date: str) -> list[Environment]:
        in_placeholders = ", ".join("?" * len(names))
        with self.connection:
            res = self.connection.execute(
                f"""SELECT name, timestamp, humidity, temperature 
                FROM environment 
                WHERE name in ({in_placeholders}) 
                AND timestamp >= ? AND timestamp < ?;""",
                (*names, from_date, to_date)
                )
        readings = res.fetchall()

        formatted_readings = [Environment(
            name=n, timestamp=ts, humidity=hmd, temperature=tmp
            ) for n, ts, hmd, tmp in readings]           

        return formatted_readings

    def select_plants(self, names: list[str], from_date: str, to_date: str) -> list[Plant]:
        in_placeholders = ", ".join("?" * len(names))
        with self.connection:
            res = self.connection.execute(
                f"""SELECT name, timestamp, moisture_percent, moisture_voltage
                FROM plant WHERE name in ({in_placeholders})
                AND timestamp >= ? AND timestamp < ?;""",
                (*names, from_date, to_date)
                )
        readings = res.fetchall()

        formatted_readings = [Plant(
            name=n, timestamp=ts, moisture_percent=mp, moisture_voltage=mv
            ) for n, ts, mp, mv in readings]

        return formatted_readings

    def close(self):
        self.connection.close()

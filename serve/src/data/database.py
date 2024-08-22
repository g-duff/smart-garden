import sqlite3
import configparser

from .objects import Location, Plant

class Database:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        database_path = config['SQLite3']['Path']

        self.connection = sqlite3.connect(database_path)

    def insert_plant(self, name, timestamp, moisture_percent, moisture_voltage):
        with self.connection:
            self.connection.execute("""INSERT INTO plant 
                (timestamp, name, moisture_percent, moisture_voltage) 
                VALUES (?, ?, ?, ?);""",
                (timestamp, name, moisture_percent, moisture_voltage),
                )

    def insert_loctation(self, name, timestamp, humidity, temperature):
        with self.connection:
            self.connection.execute(f"""INSERT INTO location 
                (timestamp, name, humidity, temperature) 
                VALUES (?, ?, ?, ?);""",
                (timestamp, name, humidity, temperature)
                )

    def select_locations(self, names: list[str], from_date: str, to_date: str) -> list[Location]:
        in_placeholders = ", ".join("?" * len(names))
        with self.connection:
            res = self.connection.execute(
                f"""SELECT name, timestamp, humidity, temperature 
                FROM location 
                WHERE name in ({in_placeholders}) 
                AND timestamp >= ? AND timestamp < ?;""",
                (*names, from_date, to_date)
                )
        readings = res.fetchall()

        formatted_readings = [Location(
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

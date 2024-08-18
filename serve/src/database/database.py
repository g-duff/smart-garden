import sqlite3
import configparser


class Database:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        database_path = config['SQLite3']['Path']

        self.connection = sqlite3.connect(database_path)

    def insert_plant(self, name, timestamp, moisture_percent, moisture_voltage):
        with self.connection:
            self.connection.execute(f"""INSERT INTO plant 
                (timestamp, "name", moisture_percent, moisture_voltage) 
                VALUES (\"{timestamp}\", \"{name}\", {moisture_percent:.0f}, {moisture_voltage:.2f});
                """)

    def insert_loctation(self, name, timestamp, humidity, temperature):
        with self.connection:
            self.connection.execute(f"""INSERT INTO location 
                (timestamp, "name", humidity, temperature) 
                VALUES (\"{timestamp}\", \"{name}\", {humidity:0.2f}, {temperature:0.1f});
            """)

    def select_locations(self, names: list[str], from_date: str, to_date: str):
        in_placeholders = ", ".join("?" * len(names))
        with self.connection:
            res = self.connection.execute(
                f"""SELECT timestamp, humidity, temperature 
                FROM location 
                WHERE name in ({in_placeholders}) 
                AND timestamp >= ? AND timestamp < ?;""",
                (*names, from_date, to_date)
                )
        readings = res.fetchall()

        formatted_readings = [{
            "timestamp": timestamp,
            "humidity": humidity,
            "temperature": temperature,
            } for timestamp, humidity, temperature in readings]           

        return formatted_readings

    def select_plants(self, names: list[str], from_date: str, to_date: str):
        in_placeholders = ", ".join("?" * len(names))
        with self.connection:
            res = self.connection.execute(
                f"""SELECT timestamp, moisture_percent, moisture_voltage
                FROM plant WHERE name in ({in_placeholders})
                AND timestamp >= ? AND timestamp < ?;""",
                (*names, from_date, to_date)
                )
        readings = res.fetchall()

        formatted_readings = [{
            "timestamp": timestamp,
            "moisture_percent": moisture_percent,
            "moisture_voltage": moisture_voltage,
            } for timestamp, moisture_percent, moisture_voltage in readings]

        return formatted_readings

    def close(self):
        self.connection.close()

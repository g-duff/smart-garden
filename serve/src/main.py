import datetime
import sqlite3

from flask import Flask, request

app = Flask(__name__)


DATABASE_PATH = "/home/pi/smart-garden/store/garden.db"


@app.route("/json/plant/<name>", methods=["GET", "POST"])
def plant(name):
    match request.method:
        case "GET":
            return {}
        case "POST":
            return {}


@app.route("/json/location/<name>", methods=["GET", "POST"])
def location(name):
    match request.method:
        case "GET":
            from_date = request.args.get('from', datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat())
            to_date = request.args.get('to', datetime.datetime.now().isoformat())

            database_connection = sqlite3.connect("/home/pi/smart-garden/store/garden.db")
            with database_connection:
                res = database_connection.execute(f"SELECT timestamp, humidity, temperature FROM location WHERE name = \'{name}\' and timestamp >= '{from_date}' and timestamp < '{to_date}';")
                readings = res.fetchall()
            database_connection.close()

            formatted_readings = [{
                "timestamp": timestamp,
                "humidity": humidity,
                "temperature": temperature,
                } for timestamp, humidity, temperature in readings]           

            return formatted_readings
        case "POST":
            content = request.json

            if "humidity" not in content \
                    or "timestamp" not in content \
                    or "temperature" not in content:
                return {"error": "missing parameter"}, 400

            humidity = content["humidity"]
            temperature = content["temperature"]
            timestamp = content["timestamp"]

            database_connection = sqlite3.connect("/home/pi/smart-garden/store/garden.db")
            with database_connection:
                database_connection.execute(f"""INSERT INTO location 
                    (timestamp, "name", humidity, temperature) 
                    VALUES (\"{timestamp}\", \"{name}\", {humidity:0.2f}, {temperature:0.1f});
                """)
            database_connection.close()

            return {}


if __name__ == '__main__':
    app.run(host="0.0.0.0")

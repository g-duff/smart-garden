import datetime
import sqlite3

from flask import Flask, request

from database.database import Database

app = Flask(__name__)


DATABASE_PATH = "/home/pi/smart-garden/store/garden.db"


@app.route("/json/plant/<name>", methods=["GET", "POST"])
def plant(name):
    match request.method:
        case "GET":
            from_date = request.args.get('from', datetime.datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
                ).isoformat())
            to_date = request.args.get('to', datetime.datetime.now().isoformat())

            database_connection = Database()
            formatted_readings = database_connection.select_plants([name], from_date, to_date)
            database_connection.close()

            return formatted_readings

        case "POST":
            content = request.json
            app.logger.debug(content)

            if "timestamp" not in content \
                    or "moisture_percent" not in content \
                    or "moisture_voltage" not in content:
                return {"error": "missing parameter"}, 400

            database_connection = Database()
            database_connection.insert_plant(name,
                moisture_percent = content["moisture_percent"],
                moisture_voltage = content["moisture_voltage"],
                timestamp = content["timestamp"],
            )
            database_connection.close()

            return ('', 204)


@app.route("/json/location/<name>", methods=["GET", "POST"])
def location(name):
    match request.method:
        case "GET":
            from_date = request.args.get('from', datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat())
            to_date = request.args.get('to', datetime.datetime.now().isoformat())

            database_connection = Database()
            formatted_readings = database_connection.select_locations([name], from_date, to_date)
            database_connection.close()

            return formatted_readings
        case "POST":
            content = request.json
            app.logger.debug(content)

            if "humidity" not in content \
                    or "timestamp" not in content \
                    or "temperature" not in content:
                return {"error": "missing parameter"}, 400

            database_connection = Database()
            database_connection.insert_loctation(
                name, 
                temperature = content["temperature"],
                timestamp = content["timestamp"],
                humidity = content["humidity"],
                )
            database_connection.close()

            return ('', 204)


if __name__ == '__main__':
    app.run(host="0.0.0.0")

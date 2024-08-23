import datetime

from flask import Flask, request

from data.database import Database
from data.objects import Plant

app = Flask(__name__)


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

            plants = []
            try:
                plants.append(Plant(name, **content))
            except TypeError:
                return ({"error": "missing parameter"}, 400)

            database_connection = Database()
            database_connection.insert_plants(plants)
            database_connection.close()

            return ('', 204)


@app.route("/json/environment/<name>", methods=["GET", "POST"])
def environment(name):
    match request.method:
        case "GET":
            from_date = request.args.get('from', datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat())
            to_date = request.args.get('to', datetime.datetime.now().isoformat())

            database_connection = Database()
            formatted_readings = database_connection.select_environments([name], from_date, to_date)
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
            database_connection.insert_environment(
                name, 
                temperature = content["temperature"],
                timestamp = content["timestamp"],
                humidity = content["humidity"],
                )
            database_connection.close()

            return ('', 204)


if __name__ == '__main__':
    app.run(host="0.0.0.0")

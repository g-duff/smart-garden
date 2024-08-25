import datetime

from flask import Flask, request, render_template

from data.database import Database
from data.objects import Environment, Plant

app = Flask(__name__)


@app.route("/plant/<name>/json", methods=["GET", "POST"])
def plant_json(name):
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

            return ({"message": "created"}, 201)


@app.route("/environment/<name>/json", methods=["GET", "POST"])
def environment_json(name):
    match request.method:
        case "GET":
            from_date = request.args.get('from', datetime.datetime.now().replace(
                hour=0, minute=0, second=0, microsecond=0
                ).isoformat())
            to_date = request.args.get('to', datetime.datetime.now().isoformat())

            database_connection = Database()
            formatted_readings = database_connection.select_environments([name], from_date, to_date)
            database_connection.close()

            return formatted_readings

        case "POST":
            content = request.json
            app.logger.debug(content)

            envrionments = []
            try:
                envrionments.append(Environment(name, **content))
            except TypeError:
                return ({"error": "missing parameter"}, 400)

            database_connection = Database()
            database_connection.insert_environments(envrionments)
            database_connection.close()

            return ({"message": "created"}, 201)


@app.route("/environment/<name>/chart", methods=["GET"])
def environment_chart(name):
    from_date = request.args.get('from', datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
        ).isoformat())
    to_date = request.args.get('to', datetime.datetime.now().isoformat())

    database_connection = Database()
    formatted_readings = database_connection.select_environments([name], from_date, to_date)
    database_connection.close()

    return render_template('./environment.html', rawEnvironmentData=formatted_readings)


@app.route("/plant/<name>/chart", methods=["GET"])
def plant_chart(name):
    from_date = request.args.get('from', datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
        ).isoformat())
    to_date = request.args.get('to', datetime.datetime.now().isoformat())

    database_connection = Database()
    formatted_readings = database_connection.select_plants([name], from_date, to_date)
    database_connection.close()

    return render_template('./plant.html', rawPlantData=formatted_readings)


if __name__ == '__main__':
    app.run(host="0.0.0.0")

import configparser
import json
import logging
import urllib.request


logger = logging.getLogger(__name__)

def write_plant_data(name, timestamp, moisture_percent, moisture_voltage):
    config = configparser.ConfigParser()
    config.read('config.ini')
    hostname = config['Server']['Host']

    body = {
        "timestamp": timestamp,
        "moisture_percent": moisture_percent,
        "moisture_voltage": moisture_voltage,
    }
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

    req = urllib.request.Request(f"http://{hostname}/json/plant/{name}")
    req.add_header('Content-Type', 'application/json; charset=utf-8')

    response = urllib.request.urlopen(req, jsondataasbytes)
    logger.info(f'{response.status}: {response.reason}')

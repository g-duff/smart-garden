import configparser
import json
import logging
import urllib.request


logger = logging.getLogger(__name__)

def write_environment_data(name, timestamp, humidity, temperature):
    config = configparser.ConfigParser()
    config.read('config.ini')
    hostname = config['Server']['Host']

    body = {
        "timestamp": timestamp,
        "humidity": humidity,
        "temperature": temperature,
    }
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

    req = urllib.request.Request(f"http://{hostname}/json/environment/{name}")
    req.add_header('Content-Type', 'application/json; charset=utf-8')

    response = urllib.request.urlopen(req, jsondataasbytes)
    logger.info(f'{response.status}: {response.reason}')

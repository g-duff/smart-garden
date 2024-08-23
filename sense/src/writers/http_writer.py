import configparser
import json
import logging
import urllib.request


logger = logging.getLogger(__name__)


class HttpWriter:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.hostname = config['Server']['Host']

    def write_environment(self, name, timestamp, humidity, temperature):
        body = {
            "timestamp": timestamp,
            "humidity": humidity,
            "temperature": temperature,
        }
        self._write('environment', name, body)

    def write_plant(self, name, timestamp, moisture_percent, moisture_voltage):
        body = {
            "timestamp": timestamp,
            "moisture_percent": moisture_percent,
            "moisture_voltage": moisture_voltage,
        }
        self._write('plant', name, body)

    def _write(self, object_type, name, data):
        jsondata = json.dumps(data)
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    
        req = urllib.request.Request(f"http://{self.hostname}/json/{object_type}/{name}")
        req.add_header('Content-Type', 'application/json; charset=utf-8')
    
        response = urllib.request.urlopen(req, jsondataasbytes)
        logger.info(f'{response.status}: {response.reason}')

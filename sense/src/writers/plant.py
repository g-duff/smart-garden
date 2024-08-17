import json
import logging
import urllib.request

logger = logging.getLogger(__name__)

def write_plant_data(timestamp, moisture_percent, moisture_voltage):
    body = {
        "timestamp": timestamp,
        "moisture_percent": moisture_percent,
        "moisture_voltage": moisture_voltage,
    }
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

    req = urllib.request.Request("http://localhost:5000/json/plant/basil")
    req.add_header('Content-Type', 'application/json; charset=utf-8')

    response = urllib.request.urlopen(req, jsondataasbytes)
    logger.info(f'{response.status}: {response.reason}')

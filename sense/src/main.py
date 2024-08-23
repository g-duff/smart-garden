from datetime import datetime
import logging

from readers.humidity import read_humidity
from readers.moisture import read_moisture
from readers.temperature import read_temperature
from writers.http_writer import HttpWriter


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Started')

    writer = HttpWriter()

    humidity = read_humidity()
    temperature = read_temperature()
    writer.write_environment(
            'kitchen',
            timestamp=datetime.now().isoformat(),
            humidity=humidity if humidity else 0,
            temperature=temperature if temperature else 0,
    )

    moisture_1_percent, moisture_1_voltage = read_moisture(1)
    writer.write_plant(
            'basil',
            timestamp=datetime.now().isoformat(),
            moisture_percent=moisture_1_percent,
            moisture_voltage=moisture_1_voltage,
    )

    moisture_2_percent, moisture_2_voltage = read_moisture(2)
    writer.write_plant(
            'rosemary',
            timestamp=datetime.now().isoformat(),
            moisture_percent=moisture_2_percent,
            moisture_voltage=moisture_2_voltage,
    )

    logger.info('Finished')

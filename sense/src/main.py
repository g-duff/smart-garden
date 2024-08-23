from datetime import datetime
import logging

from readers.temperature import read_temperature
from readers.humidity import read_humidity
from readers.moisture import read_moisture

from writers.environment import write_environment_data
from writers.plant import write_plant_data


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Started')

    humidity = read_humidity()
    temperature = read_temperature()

    write_environment_data(
            'kitchen',
            timestamp=datetime.now().isoformat(),
            humidity=humidity if humidity else 0,
            temperature=temperature if temperature else 0,
    )

    moisture_1_percent, moisture_1_voltage = read_moisture(1)
    write_plant_data(
            'basil',
            timestamp=datetime.now().isoformat(),
            moisture_percent=moisture_1_percent,
            moisture_voltage=moisture_1_voltage,
    )

    moisture_2_percent, moisture_2_voltage = read_moisture(2)
    write_plant_data(
            'rosemary',
            timestamp=datetime.now().isoformat(),
            moisture_percent=moisture_2_percent,
            moisture_voltage=moisture_2_voltage,
    )

    logger.info('Finished')

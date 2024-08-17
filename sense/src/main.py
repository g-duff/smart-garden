from datetime import datetime
import logging

from readers.temperature import read_temperature
from readers.humidity import read_humidity
from readers.moisture import read_moisture

from writers.location import write_location_data
from writers.plant import write_plant_data


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('Started')

    humidity = read_humidity()
    temperature = read_temperature()

    write_location_data(
            timestamp=datetime.now().isoformat(),
            humidity=humidity if humidity else 0,
            temperature=temperature if temperature else 0,
    )

    moisture_0_percent, moisture_0_voltage = read_moisture(0)
    write_plant_data(
            timestamp=datetime.now().isoformat(),
            moisture_percent=moisture_0_percent,
            moisture_voltage=moisture_0_voltage,
    )

    logger.info('Finished')

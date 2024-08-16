from dataclasses import dataclass
import logging

from readers.temperature import read_temperature
from readers.humidity import read_humidity
from readers.moisture import read_moisture


@dataclass
class SensorData:
    humidity: float
    moisture_0: float
    moisture_1: float
    temperature: float


def read() -> SensorData: 
    humidity = read_humidity()
    moisture_0 = read_moisture(0)
    moisture_1 = read_moisture(1)
    temperature = read_temperature()

    return SensorData(
            humidity=humidity if humidity is float else 0,
            moisture_0=moisture_0,
            moisture_1=moisture_1,
            temperature=temperature if temperature is float else 0,
        )


def write(data: SensorData):
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('Started')
    data = read()
    write(data)
    

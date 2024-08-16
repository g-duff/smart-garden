from dataclasses import dataclass
import logging

from readers.temperature import read_temperature
from readers.humidity import read_humidity


@dataclass
class SensorData:
    temperature: float
    humidity: float
    moisture_plant1: float
    moisture_plant2: float


def read() -> SensorData: 
    temperature = read_temperature()
    humidity = read_humidity()

    return SensorData(
            temperature=temperature if temperature is float else 0,
            humidity=humidity if humidity is float else 0,
            moisture_plant1=0,
            moisture_plant2=0
        )


def write(data: SensorData):
    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Started')
    data = read()
    write(data)
    

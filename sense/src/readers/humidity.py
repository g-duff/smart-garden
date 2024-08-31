import logging
import time
from typing import Optional

import adafruit_dht
import board


logger = logging.getLogger(__name__)


def read_humidity() -> Optional[int|float]:
    sensor = adafruit_dht.DHT11(board.D4)

    while True:
        try:
            logger.info('Reading humidity...')
            humidity = sensor.humidity
            sensor.exit()
            logger.info(f'Humidity: {humidity}')
            return humidity

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, log and keep going
            logger.warning(str(error))
            time.sleep(2.0)
            continue

        except Exception as error:
            logger.error(error)
            sensor.exit()
            break

        except KeyboardInterrupt:
            logger.info(f'Interrupted. Exiting...')
            sensor.exit()
            break


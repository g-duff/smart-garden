# Credit:
# https://github.com/AnaviTechnology/anavi-examples/blob/master/anavi-gardening-uhat/soil-moistore-sensors/python/soil-moistore-sensors.py
import logging

import spidev


logger = logging.getLogger(__name__)


def read_moisture(sensor_channel: float) -> tuple[float, float]:
    logger.info(f'Reading moisture channel {sensor_channel}...')

    # Enable SPI
    spi_ch = 0
    spi = spidev.SpiDev(0, spi_ch)
    spi.max_speed_hz = 1200000

    voltage = read_voltage(spi, sensor_channel)
    rounded_voltage = round(voltage, 2)
    logger.debug(f'Voltage: {voltage}')
    if rounded_voltage < 0.5:
        moisture = 0
    else:
        moisture = round(voltage_to_moisture(rounded_voltage, 5, 3.5, 0, 100), 0)
    logger.info(f'Moisture: {moisture}')
    return moisture, voltage


def read_voltage(spi, channel):

    # Make sure ADC channel is 0 or 1
    if channel != 0:
        channel = 1

    # Construct SPI message
    #  First bit (Start): Logic high (1)
    #  Second bit (SGL/DIFF): 1 to select single mode
    #  Third bit (ODD/SIGN): Select channel (0 or 1)
    #  Fourth bit (MSFB): 0 for LSB first
    #  Next 12 bits: 0 (don't care)
    msg = 0b11
    msg = ((msg << 1) + channel) << 5
    msg = [msg, 0b00000000]
    reply = spi.xfer2(msg)

    # Construct single integer out of the reply (2 bytes)
    adc = 0
    for n in reply:
        adc = (adc << 8) + n

    # Last bit (0) is not part of ADC value, shift to remove it
    adc = adc >> 1

    # Calculate voltage form ADC value
    # considering the soil moisture sensor is working at 5V
    voltage = (5 * adc) / 1024

    return voltage


def voltage_to_moisture(value, istart, istop, ostart, ostop):
    value = ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
    if value > ostop:
       value = ostop
    return value

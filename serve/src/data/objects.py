from dataclasses import dataclass


@dataclass
class Location:
    name: str
    timestamp: str
    temperature: float
    humidity: float


@dataclass
class Plant:
    name: str
    timestamp: str
    moisture_percent: float
    moisture_voltage: float


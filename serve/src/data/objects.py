from dataclasses import dataclass


@dataclass
class Location:
    name: str
    timestamp: str
    humidity: float
    temperature: float


@dataclass
class Plant:
    name: str
    timestamp: str
    moisture_percent: float
    moisture_voltage: float


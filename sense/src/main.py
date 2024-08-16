from dataclasses import dataclass


@dataclass
class SensorData:
    temperature: float
    humidity: float
    moisture_plant1: float
    moisture_plant2: float


def read() -> SensorData: 
    return SensorData(
            temperature=0,
            humidity=0,
            moisture_plant1=0,
            moisture_plant2=0
        )


def write(data: SensorData):
    pass


if __name__ == '__main__':
    data = read()
    write(data)
    

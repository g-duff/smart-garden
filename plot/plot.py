import pandas as pd
import matplotlib.pyplot as plt

host = 'http://pi-0.local:5000'

location_df = pd.read_json(f'{host}/environment/kitchen/json', orient='records', convert_dates=True)
plant_df = pd.read_json(f'{host}/plant/basil/json', orient='records', convert_dates=True)

fig, (mst_ax, hmd_ax, tmp_ax) = plt.subplots(nrows=3, sharex=True)

mst_ax.plot(plant_df['timestamp'], plant_df['moisture_percent'], marker='o')
mst_ax.set_ylabel('Moisture (%)')

hmd_ax.plot(location_df['timestamp'], location_df['humidity'], marker='o')
hmd_ax.set_ylabel('Humidity (%)')

tmp_ax.plot(location_df['timestamp'], location_df['temperature'], marker='o')
tmp_ax.set_ylabel(u'Temperature (\N{DEGREE SIGN}C)')
tmp_ax.set_xlabel('Timestamp')
tmp_ax.tick_params(axis='x', rotation=30)

fig.tight_layout()

plt.show()

import random
import time
import json
from pathlib import Path


# Find project data folder automatically
data_folder = Path(__file__).parent.parent / "data"
data_folder.mkdir(exist_ok=True)


sensor_file = data_folder / "sensor_data.json"


# Different production speeds for each station
station_probabilities = [
    0.90,  # Station 1
    0.85,  # Station 2
    0.95,  # Station 3
    0.70,  # Station 4
    0.8,  # Station 5
    0.90   # Station 6
]


print("Six station sensor simulator running...")


while True:

    # Read current data
    with open(sensor_file, "r") as file:
        data = json.load(file)


    # Check each station sensor
    for i, station in enumerate(data["stations"]):

        if random.random() < station_probabilities[i]:

            print(
                f"{station['name']}: PART_DETECTED"
            )

            station["count"] += 1

            station["signal"] = "PART_DETECTED"

        else:

            station["signal"] = "IDLE"



    # Write updated data
    with open(sensor_file, "w") as file:

        json.dump(
            data,
            file,
            indent=4
        )


    # Sensor scan interval
    time.sleep(0.5)

import time
import json
from pathlib import Path


# File locations
project_folder = Path(__file__).parent.parent
sensor_file = project_folder / "data" / "sensor_data.txt"
dashboard_file = project_folder / "data" / "dashboard_data.json"


total_parts = 0


def update_dashboard():

    dashboard_data = {
        "stations": [
            {
                "name": "Station 1",
                "count": total_parts,
                "status": "RUNNING"
            }
        ]
    }

    with open(dashboard_file, "w") as file:
        json.dump(dashboard_data, file, indent=4)


def check_sensor_file():

    global total_parts

    if sensor_file.exists():

        with open(sensor_file, "r") as file:
            lines = file.readlines()

        if len(lines) > total_parts:
            total_parts = len(lines)


print("Production counter running...")


while True:

    check_sensor_file()

    update_dashboard()

    print("-------------------")
    print(f"Total Parts: {total_parts}")
    print("-------------------")

    time.sleep(1)
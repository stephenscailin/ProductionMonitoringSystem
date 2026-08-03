import time
import json
from pathlib import Path


# -----------------------------
# Settings
# -----------------------------

TARGET_RATE = 6  # parts per minute

RATE_WINDOW = 10  # seconds for testing


# -----------------------------
# File Locations
# -----------------------------

project_folder = Path(__file__).parent.parent

sensor_file = (
    project_folder /
    "data" /
    "sensor_data.json"
)

dashboard_file = (
    project_folder /
    "data" /
    "dashboard_data.json"
)


# -----------------------------
# Rate Tracking Memory
# -----------------------------

previous_counts = {}

start_time = time.time()



print("Production monitoring system running...")



def calculate_rate(station_name, current_count):

    global previous_counts
    global start_time


    current_time = time.time()

    elapsed = current_time - start_time


    # Wait until the rate window is reached
    if elapsed < RATE_WINDOW:

        if station_name not in previous_counts:
            previous_counts[station_name] = current_count

        return 0


    previous_count = previous_counts.get(
        station_name,
        current_count
    )


    parts_made = current_count - previous_count


    # Convert to parts/min
    rate = (
        parts_made /
        elapsed
    ) * 60


    # Reset measurement
    previous_counts[station_name] = current_count


    return round(rate, 2)



def update_dashboard():

    with open(sensor_file, "r") as file:

        sensor_data = json.load(file)



    dashboard_stations = []


    print("-------------------------")



    for station in sensor_data["stations"]:


        rate = calculate_rate(
            station["name"],
            station["count"]
        )


        if rate >= TARGET_RATE:

            status = "RUNNING"

        else:

            status = "LOW OUTPUT"



        print(
            station["name"]
        )

        print(
            "Count:",
            station["count"]
        )

        print(
            "Rate:",
            rate,
            "parts/min"
        )

        print(
            "Status:",
            status
        )

        print()



        dashboard_stations.append(
            {
                "name": station["name"],
                "count": station["count"],
                "status": status
            }
        )



    dashboard_data = {

        "stations": dashboard_stations

    }



    with open(
        dashboard_file,
        "w"
    ) as file:

        json.dump(
            dashboard_data,
            file,
            indent=4
        )



while True:

    try:

        update_dashboard()


    except Exception as e:

        print(
            "Production Counter Error:",
            e
        )


    time.sleep(1)
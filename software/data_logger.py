import time
import json
import csv
from pathlib import Path
from datetime import datetime


# -----------------------------
# File Locations
# -----------------------------

project_folder = Path(__file__).parent.parent

dashboard_file = (
    project_folder /
    "data" /
    "dashboard_data.json"
)

log_file = (
    project_folder /
    "data" /
    "production_log.csv"
)


# -----------------------------
# Create CSV if it doesn't exist
# -----------------------------

if not log_file.exists():

    with open(
        log_file,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "Timestamp",
                "Station",
                "Count",
                "Rate",
                "Status"
            ]
        )


print("Production data logger running...")



# -----------------------------
# Logging Loop
# -----------------------------

while True:

    try:

        with open(
            dashboard_file,
            "r"
        ) as file:

            data = json.load(file)



        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )



        with open(
            log_file,
            "a",
            newline=""
        ) as file:

            writer = csv.writer(file)


            for station in data["stations"]:

                writer.writerow(
                    [
                        timestamp,
                        station["name"],
                        station["count"],
                        station.get("rate", 0),
                        station["status"]
                    ]
                )



        print(
            f"Logged data at {timestamp}"
        )


    except Exception as e:

        print(
            "Logger Error:",
            e
        )


    # Log every 10 seconds
    time.sleep(10)
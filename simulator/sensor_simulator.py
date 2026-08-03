import random
import time
from pathlib import Path

# Find the project data folder automatically
data_folder = Path(__file__).parent.parent / "data"
data_folder.mkdir(exist_ok=True)

sensor_file = data_folder / "sensor_data.txt"

print("Photoeye simulator running...")

while True:

    # Simulates a product passing the photoeye
    # 30% chance every 0.1 seconds
    if random.random() < 0.3:
        print("PART_DETECTED")

        with open(sensor_file, "a") as file:
            file.write("PART_DETECTED\n")

    time.sleep(0.1)
import time
import os

total_parts = 0


def check_sensor_file():

    global total_parts

    file_path = "data/sensor_data.txt"

    if os.path.exists(file_path):

        with open(file_path, "r") as file:
            lines = file.readlines()

        if len(lines) > total_parts:
            new_parts = len(lines) - total_parts
            total_parts += new_parts


print("Production counter running...")

while True:

    check_sensor_file()

    print("-------------------")
    print(f"Total Parts: {total_parts}")
    print("-------------------")

    time.sleep(1)
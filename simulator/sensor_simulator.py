import random
import time


def detect_part():
    """
    Simulates the photoeye detecting a product.
    Returns True when a product passes the sensor.
    """

    return random.random() < 0.3


print("Photoeye simulator running...")

while True:
    if detect_part():
        print("PART_DETECTED")

    time.sleep(0.1)
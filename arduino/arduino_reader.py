"""
Arduino serial reader - real sensor input (two-sensor circuit).
 
Drop-in replacement for simulator/sensor_simulator.py: reads PART_DETECTED
events from the Arduino over serial and writes them into data/sensor_data.json
in the same format the simulator produced, so production_counter.py,
data_logger.py, and the dashboards keep working with no changes.
 
Accepts any of these line formats from the sketch:
    1,PART_DETECTED
    1, PART_DETECTED
    S1 PART_DETECTED
 
Run this INSTEAD of sensor_simulator.py once your real sensors are wired up:
 
    python arduino\\arduino_reader.py
    python software\\production_counter.py     (separate terminal)
    python software\\dashboard.py              (separate terminal)
 
Stop it with Ctrl+C BEFORE uploading a new sketch (it holds the port).
"""
 
import json
import os
import time
from pathlib import Path
 
import serial
import serial.tools.list_ports
 
 
# -----------------------------
# Settings - edit these for your setup
# -----------------------------
 
# "AUTO" looks for the Arduino by itself (handy since Windows keeps changing
# the COM number). If it can't find it, type the port in, e.g. "COM6".
SERIAL_PORT = "AUTO"
 
BAUD_RATE = 9600             # must match Serial.begin(...) in the .ino sketch
 
# Maps each sensor's tag to the station it feeds in sensor_data.json.
# Add more entries here as you wire up more sensors.
SENSOR_STATIONS = {
    "S1": "Station 1",
    "S2": "Station 2",
    "S3": "Station 3",
    "S4": "Station 4",
    "S5": "Station 5",
}
 
PART_DEBOUNCE_TIME = 0.15    # seconds - ignore repeat detections closer than this (per station)
SIGNAL_HOLD_TIME = 1.0       # seconds - keep PART_DETECTED showing so the dashboard can see it
 
 
# -----------------------------
# File Location
# -----------------------------
 
project_folder = Path(__file__).parent.parent
 
sensor_file = project_folder / "data" / "sensor_data.json"
 
 
# -----------------------------
# Helpers
# -----------------------------
 
def default_data():
 
    return {
        "stations": [
            {"name": f"Station {i + 1}", "count": 0, "signal": "IDLE"}
            for i in range(6)
        ]
    }
 
 
def read_sensor_data():
    """Read sensor_data.json, or build a fresh one if it's missing or damaged."""
 
    try:
        with open(sensor_file, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_data()
 
 
def write_sensor_data(data):
    """Write to a temp file, then swap it in, so the counter never reads a half-written file."""
 
    temp_file = sensor_file.with_suffix(".tmp")
 
    with open(temp_file, "w") as file:
        json.dump(data, file, indent=4)
 
    for _ in range(10):
        try:
            os.replace(temp_file, sensor_file)
            return
        except PermissionError:      # file briefly locked (OneDrive, dashboard, etc.)
            time.sleep(0.05)
 
    print("WARNING: could not save sensor_data.json (file locked - OneDrive?)")
 
 
def find_port():
    """Look for an Arduino-like serial port."""
 
    for port in serial.tools.list_ports.comports():
        description = f"{port.description} {port.manufacturer or ''}".lower()
        if any(word in description for word in ("arduino", "ch340", "usb serial")):
            return port.device
 
    return None
 
 
def connect():
 
    port = SERIAL_PORT
 
    if port == "AUTO":
        port = find_port()
        if port is None:
            raise serial.SerialException(
                'No Arduino found. Set SERIAL_PORT at the top of the file, e.g. "COM6".'
            )
 
    print(f"Connecting to Arduino on {port}...")
 
    connection = serial.Serial(port, BAUD_RATE, timeout=0.2)
 
    time.sleep(2)  # let the Arduino finish its reset after the port opens
 
    connection.reset_input_buffer()
 
    return connection
 
 
# -----------------------------
# Main Loop
# -----------------------------
 
arduino = connect()
 
print(f"Arduino reader running. Feeding {list(SENSOR_STATIONS.values())}. "
      "Waiting for PART_DETECTED events...")
 
last_part_time = {}      # tag -> time of last counted part
last_signal_time = {}    # station name -> when PART_DETECTED was last shown
 
 
while True:
 
    try:
 
        line = arduino.readline().decode("utf-8", errors="ignore").strip()
 
        now = time.time()
 
 
        # ---- New detection from the Arduino ----
        if line:
 
            # Accepts "1,PART_DETECTED", "1, PART_DETECTED" or "S1 PART_DETECTED"
            cleaned = line.replace(",", " ").split()
 
            if len(cleaned) == 2 and cleaned[1] == "PART_DETECTED":
 
                tag = "S" + cleaned[0].upper().lstrip("S")
 
                not_a_repeat = now - last_part_time.get(tag, 0) >= PART_DEBOUNCE_TIME
 
                if tag in SENSOR_STATIONS and not_a_repeat:
 
                    station_name = SENSOR_STATIONS[tag]
 
                    last_part_time[tag] = now
                    last_signal_time[station_name] = now
 
                    data = read_sensor_data()
 
                    for station in data["stations"]:
 
                        if station["name"] == station_name:
 
                            station["count"] += 1
                            station["signal"] = "PART_DETECTED"
 
                            new_count = station["count"]
 
                    write_sensor_data(data)
 
                    print(f"{station_name}: PART_DETECTED (count {new_count})")
 
            # Any other line (startup messages, unknown tags) is ignored.
 
 
        # ---- Return stations to IDLE once the hold time has passed ----
        expired = [
            name for name, t in last_signal_time.items()
            if now - t >= SIGNAL_HOLD_TIME
        ]
 
        if expired:
 
            data = read_sensor_data()
 
            for station in data["stations"]:
 
                if station["name"] in expired:
                    station["signal"] = "IDLE"
 
            write_sensor_data(data)
 
            for name in expired:
                del last_signal_time[name]
 
 
    except serial.SerialException as e:
 
        print("Serial connection lost:", e)
        print("Retrying in 3 seconds...")
 
        time.sleep(3)
 
        try:
            arduino = connect()
        except Exception as reconnect_error:
            print("Reconnect failed:", reconnect_error)
 
    except KeyboardInterrupt:
 
        print("Stopped.")
        break
 
    except Exception as e:
 
        print("Reader Error:", e)
        time.sleep(1)

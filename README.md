# Production Monitoring System

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)
![PyQtGraph](https://img.shields.io/badge/Charts-PyQtGraph-orange)
![Status](https://img.shields.io/badge/Status-Prototype-yellow)

A Python-based production monitoring system that simulates real-time manufacturing data and displays live production metrics through an interactive dashboard. The project demonstrates how production data can be collected, processed, and visualized in a modular application.

> **Note:** The current version uses a software-based sensor simulator. The simulator is designed to be replaced with live input from an Arduino, PLC, or other industrial controller.

---

## Features

* Real-time monitoring of six production stations
* Simulated production sensors
* Automatic part counting
* Production rate calculations (parts per minute)
* Live production status monitoring
* Interactive dashboard built with PyQt6
* Production bar chart using PyQtGraph
* Modular program design
* JSON-based communication between application modules

---

## Dashboard Overview

The dashboard displays:

* Production count for each station
* Current production status
* Live production output chart
* Automatic updates every second

---

## Project Structure

```text
ProductionMonitoringSystem/
│
├── arduino
│
├── data
│   ├── sensor_data.json
│   ├── production_log.csv
│   └── dashboard_data.json
│
├── simulator
│   └── sensor_simulator.py
│
├── software
│   ├── production_counter.py
│   ├── dashboard.py
│   ├── dashboard_v2.py
│   ├── station_card.py
│   ├──history_dashboard.py
│   ├── data_logger.py
│   └── production_chart.py
│
└── README.md
```

---

## How It Works

The application consists of three main components.

### 1. Sensor Simulator

The sensor simulator generates random production events to imitate six independent production stations.

Functions:

* Simulates sensor activity
* Detects parts
* Increments production counts
* Updates station signals
* Saves data to `sensor_data.json`

---

### 2. Production Counter

The production counter continuously reads the simulated sensor data and calculates production performance.

Functions:

* Reads production counts
* Calculates production rate (parts/minute)
* Compares production rate against a target value
* Determines station status
* Writes processed data to `dashboard_data.json`

---

### 3. Production Dashboard

The dashboard provides a live graphical display of production information.

Features include:

* Station information cards
* Live production counts
* Color-coded production status
* Real-time production chart

---

## System Workflow

```text
Sensor Simulator
        │
        ▼
sensor_data.json
        │
        ▼
Production Counter
        │
        ▼
dashboard_data.json
        │
        ▼
PyQt6 Dashboard
```

---

## Technologies Used

* Python 3
* PyQt6
* PyQtGraph
* JSON
* pathlib

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/ProductionMonitoringSystem.git
```

Navigate to the project folder:

```bash
cd ProductionMonitoringSystem
```

Install the required packages:

```bash
pip install pyqt6 pyqtgraph
```

---

## Running the Project

Open **three terminal windows**.

### Terminal 1

Run the sensor simulator.

```bash
python sensor_simulator.py
```

### Terminal 2

Run the production counter.

```bash
python production_counter.py
```

### Terminal 3

Launch the dashboard.

```bash
python dashboard.py
```

---

## Production Status Logic

| Production Rate                      | Status        |
| ------------------------------------ | ------------- |
| Greater than or equal to target rate | 🟢 RUNNING    |
| Below target rate                    | 🔴 LOW OUTPUT |

---

## Current Data Flow

```
Sensor Input
      ↓
Sensor Simulator
      ↓
sensor_data.json
      ↓
Production Counter
      ↓
dashboard_data.json
      ↓
Dashboard Interface
```

---

## Future Improvements

* Replace simulated sensors with Arduino input
* Support PLC communication
* Calculate Overall Equipment Effectiveness (OEE)
* Generate daily and shift production reports
* Add production alarms and notifications
* Support multiple production lines
* Improve dashboard responsiveness

---

## Project Purpose

This project was developed to demonstrate practical software engineering concepts within a manufacturing environment, including:

* Python programming
* Object-Oriented Programming (OOP)
* GUI development with PyQt6
* Real-time data processing
* Industrial automation concepts
* Manufacturing data visualization
* Modular software architecture
* File-based data communication

Although this version uses simulated production data, the software architecture allows the sensor simulator to be replaced with real hardware inputs such as Arduino-based sensors, PLCs, or industrial controllers with minimal changes to the rest of the application.

---

## Dashboard Preview

*Add a screenshot of your dashboard here.*

Example:

```
README.md
images/
    dashboard.png
```

Then include:

```markdown
![Dashboard Screenshot](images/dashboard.png)
```

---

## Author

**Cailin Stephens**

Developed as an Engineering Intern at Artemis Plastics to demonstrate Python programming, industrial automation concepts, and real-time production monitoring.


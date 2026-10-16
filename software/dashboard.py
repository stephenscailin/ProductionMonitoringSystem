import os
import sys
import json
import time
from pathlib import Path
 
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QSizePolicy
)
 
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
 
from station_card import StationCard
from production_chart import ProductionChart
 
 
# -----------------------------
# Data Location
# -----------------------------
 
project_folder = Path(__file__).parent.parent
 
dashboard_file = (
    project_folder /
    "data" /
    "dashboard_data.json"
)
 
sensor_file = (
    project_folder /
    "data" /
    "sensor_data.json"
)
 
 
# -----------------------------
# Main Dashboard
# -----------------------------
 
class ProductionDashboard(QWidget):
 
    def __init__(self):
 
        super().__init__()
 
        self.setWindowTitle(
            "Production Monitoring System"
        )
 
        self.resize(
            1280,
            720
        )
 
 
        self.setStyleSheet("""
            QWidget {
                background-color:#2B2B2B;
                color:white;
            }
 
            QPushButton {
                background-color:#016180;
                color:white;
                border-radius:8px;
                padding:10px;
                font-size:14px;
            }
 
            QPushButton:hover {
                background-color:#0182A8;
            }
        """)
 
 
        # -----------------------------
        # Main Layout
        # -----------------------------
 
        main_layout = QVBoxLayout()
 
 
        # -----------------------------
        # Title
        # -----------------------------
 
        title = QLabel(
            "PRODUCTION MONITORING SYSTEM"
        )
 
        title.setFont(
            QFont(
                "Segoe UI",
                20,
                QFont.Weight.Bold
            )
        )
 
        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
 
        title.setStyleSheet(
            "color:#D0D0D0;"
        )
 
 
        main_layout.addWidget(
            title
        )
 
 
        # -----------------------------
        # Reset Button (all stations)
        # -----------------------------
 
        reset_button = QPushButton(
            "RESET ALL PRODUCTION COUNTS"
        )
 
        reset_button.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Weight.Bold
            )
        )
 
 
        reset_button.clicked.connect(
            self.reset_counts
        )
 
 
        main_layout.addWidget(
            reset_button
        )
 
 
        # -----------------------------
        # Content Layout
        # -----------------------------
 
        content_layout = QHBoxLayout()
 
 
        station_panel = QVBoxLayout()
 
 
        self.station_cards = []
 
 
        station_colors = [
            "#FD7979",
            "#FFA77F",
            "#FFCC8F",
            "#7DC9FF",
            "#68A8F1",
            "#016180"
        ]
 
 
        for i in range(6):
 
            card = StationCard(
                f"Station {i+1}",
                0,
                station_colors[i]
            )
 
            self.station_cards.append(
                card
            )
 
 
            # Individual reset button for this station
            station_reset_button = QPushButton(
                "RESET"
            )
 
            station_reset_button.setFont(
                QFont(
                    "Segoe UI",
                    10,
                    QFont.Weight.Bold
                )
            )
 
            station_reset_button.setFixedWidth(
                80
            )
 
            # Stretch the button to match the card's height
            station_reset_button.setSizePolicy(
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Expanding
            )
 
            station_reset_button.clicked.connect(
                lambda checked, index=i: self.reset_station(index)
            )
 
 
            # Card on the left, its reset button on the right
            station_row = QHBoxLayout()
 
            station_row.addWidget(
                card,
                1
            )
 
            station_row.addWidget(
                station_reset_button
            )
 
 
            station_panel.addLayout(
                station_row
            )
 
 
        station_panel.addStretch()
 
 
        # -----------------------------
        # Chart
        # -----------------------------
 
        self.chart = ProductionChart()
 
 
        content_layout.addLayout(
            station_panel,
            2
        )
 
 
        content_layout.addWidget(
            self.chart,
            5
        )
 
 
        main_layout.addLayout(
            content_layout
        )
 
 
        self.setLayout(
            main_layout
        )
 
 
        # -----------------------------
        # Update Timer
        # -----------------------------
 
        self.timer = QTimer()
 
        self.timer.timeout.connect(
            self.update_dashboard
        )
 
        self.timer.start(
            1000
        )
 
 
        self.update_dashboard()
 
 
 
    # -----------------------------
    # Sensor File Helpers
    # -----------------------------
 
    def load_sensor_data(self):
 
        with open(
            sensor_file,
            "r"
        ) as file:
 
            return json.load(file)
 
 
    def save_sensor_data(self, data):
 
        # Write to a temp file, then swap it in, so nothing
        # ever reads a half-written file
        temp_file = sensor_file.with_suffix(".tmp")
 
        with open(
            temp_file,
            "w"
        ) as file:
 
            json.dump(
                data,
                file,
                indent=4
            )
 
 
        for _ in range(10):
 
            try:
 
                os.replace(
                    temp_file,
                    sensor_file
                )
 
                return
 
            except PermissionError:
 
                time.sleep(0.05)
 
 
        print(
            "Reset Error: sensor_data.json is locked, try again."
        )
 
 
 
    # -----------------------------
    # Reset One Station
    # -----------------------------
 
    def reset_station(self, index):
 
        answer = QMessageBox.question(
            self,
            "Reset Confirmation",
            f"Reset the production count for Station {index + 1}?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
 
 
        if answer != QMessageBox.StandardButton.Yes:
 
            return
 
 
        try:
 
            data = self.load_sensor_data()
 
 
            data["stations"][index]["count"] = 0
 
 
            self.save_sensor_data(
                data
            )
 
 
            print(
                f"Station {index + 1} count reset."
            )
 
 
        except Exception as e:
 
            print(
                "Reset Error:",
                e
            )
 
 
 
    # -----------------------------
    # Reset All Production Counts
    # -----------------------------
 
    def reset_counts(self):
 
        answer = QMessageBox.question(
            self,
            "Reset Confirmation",
            "Are you sure you want to reset all production counts?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )
 
 
        if answer != QMessageBox.StandardButton.Yes:
 
            return
 
 
        try:
 
            data = self.load_sensor_data()
 
 
            for station in data["stations"]:
 
                station["count"] = 0
 
 
            self.save_sensor_data(
                data
            )
 
 
            print(
                "Production counts reset."
            )
 
 
        except Exception as e:
 
            print(
                "Reset Error:",
                e
            )
 
 
 
    # -----------------------------
    # Read Dashboard JSON
    # -----------------------------
 
    def update_dashboard(self):
 
        try:
 
            with open(
                dashboard_file,
                "r"
            ) as file:
 
                data = json.load(file)
 
 
            stations = data["stations"]
 
 
            for i, station in enumerate(stations):
 
                self.station_cards[i].update_data(
                    station
                )
 
 
            self.chart.update_chart(
                stations
            )
 
 
        except Exception as e:
 
            print(
                "Dashboard Error:",
                e
            )
 
 
 
# -----------------------------
# Launch
# -----------------------------
 
app = QApplication(sys.argv)
 
window = ProductionDashboard()
 
window.show()
 
sys.exit(
    app.exec()
)
 

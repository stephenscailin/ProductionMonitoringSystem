import sys
import json
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QMessageBox
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
        # Reset Button
        # -----------------------------

        reset_button = QPushButton(
            "RESET PRODUCTION COUNT"
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

            station_panel.addWidget(
                card
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
    # Reset Production Counts
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

            with open(
                sensor_file,
                "r"
            ) as file:

                data = json.load(file)


            for station in data["stations"]:

                station["count"] = 0


            with open(
                sensor_file,
                "w"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
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
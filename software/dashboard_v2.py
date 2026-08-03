import sys
import json
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
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


# -----------------------------
# Main Dashboard
# -----------------------------

class ProductionDashboard(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Production Monitoring System"
        )

        # Windows 11 friendly size
        self.resize(
            1280,
            720
        )


        self.setStyleSheet("""
            QWidget {
                background-color:#2B2B2B;
                color:white;
            }
        """)


        # Main Layout

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
        # Content Layout
        # -----------------------------

        content_layout = QHBoxLayout()


        # LEFT SIDE - Stations

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


        # RIGHT SIDE - Chart

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
    # Read JSON
    # -----------------------------

    def update_dashboard(self):

        try:

            with open(
                dashboard_file,
                "r"
            ) as file:

                data = json.load(file)


            stations = data["stations"]


            for i,station in enumerate(stations):

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
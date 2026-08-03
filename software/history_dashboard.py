import sys
import csv
from pathlib import Path
from collections import defaultdict

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QLabel
)

from PyQt6.QtGui import QFont

import pyqtgraph as pg


# -----------------------------
# Locations
# -----------------------------

project_folder = Path(__file__).parent.parent

log_file = (
    project_folder /
    "data" /
    "production_log.csv"
)


# -----------------------------
# Station Colors
# -----------------------------

STATION_COLORS = [
    "#FD7979",
    "#FFA77F",
    "#FFCC8F",
    "#7DC9FF",
    "#68A8F1",
    "#016180"
]


# -----------------------------
# History Window
# -----------------------------

class HistoryDashboard(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Production History Report"
        )

        self.resize(
            1200,
            800
        )


        self.setStyleSheet("""
            QWidget {
                background-color:#2B2B2B;
                color:white;
            }
        """)


        layout = QGridLayout()


        title = QLabel(
            "PRODUCTION RATE HISTORY"
        )

        title.setFont(
            QFont(
                "Segoe UI",
                20,
                QFont.Weight.Bold
            )
        )


        layout.addWidget(
            title,
            0,
            0,
            1,
            2
        )


        self.load_data()


        self.graphs = []


        for i in range(6):

            graph = pg.PlotWidget()

            graph.setBackground(
                "#2B2B2B"
            )


            graph.showGrid(
                x=True,
                y=True,
                alpha=0.2
            )


            graph.setTitle(
                f"Station {i+1} Rate",
                color="#D0D0D0"
            )


            graph.setLabel(
                "left",
                "Parts / Min"
            )


            graph.setLabel(
                "bottom",
                "Samples"
            )


            # FIXED: Match dictionary keys
            graph.plot(
                self.rates[f"Station {i+1}"],
                pen=pg.mkPen(
                    STATION_COLORS[i],
                    width=3
                )
            )


            row = (i // 2) + 1
            col = i % 2


            layout.addWidget(
                graph,
                row,
                col
            )


            self.graphs.append(
                graph
            )


        self.setLayout(
            layout
        )



    # -----------------------------
    # Read CSV
    # -----------------------------

    def load_data(self):

        self.rates = defaultdict(list)


        try:

            with open(
                log_file,
                "r"
            ) as file:

                reader = csv.DictReader(file)


                for row in reader:

                    station = row["Station"]

                    rate = float(
                        row["Rate"]
                    )


                    self.rates[station].append(
                        rate
                    )


        except Exception as e:

            print(
                "History Load Error:",
                e
            )


        # Ensure all six stations exist

        self.rates = {

            f"Station {i+1}":
            self.rates[f"Station {i+1}"]

            for i in range(6)

        }



# -----------------------------
# Launch
# -----------------------------

app = QApplication(sys.argv)

window = HistoryDashboard()

window.show()

sys.exit(
    app.exec()
)
import sys
import json
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QProgressBar
)

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


# -----------------------------
# File Location
# -----------------------------

project_folder = Path(__file__).parent.parent
dashboard_file = project_folder / "data" / "dashboard_data.json"

BAR_COLORS = [
    "#FD7979",
    "#FFA77F",
    "#FFCC8F",
    "#7DC9FF",
    "#68A8F1",
    "#016180"
]


class ProductionDashboard(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Production Monitoring System")
        self.resize(1400, 800)

        self.setStyleSheet("""
            QWidget{
                background:#2B2B2B;
                color:white;
            }
        """)

        self.station_labels = []
        self.count_labels = []
        self.progress_bars = []

        main_layout = QVBoxLayout()

        # ---------- TITLE ----------
        title = QLabel("PRODUCTION MONITORING SYSTEM")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 24))

        main_layout.addWidget(title)

        # ---------- CONTENT ----------
        content = QHBoxLayout()

        # LEFT PANEL
        left = QVBoxLayout()

        # RIGHT PANEL
        right = QVBoxLayout()

        for i in range(6):

            # ---------- Station Box ----------
            card = QFrame()

            card.setStyleSheet("""
                QFrame{
                    background:#555555;
                    border-radius:12px;
                    padding:10px;
                }
            """)

            card_layout = QVBoxLayout()

            station = QLabel(f"Station {i+1}")
            station.setFont(QFont("Arial",16))

            count = QLabel("0")
            count.setFont(QFont("Arial",36))
            count.setAlignment(Qt.AlignmentFlag.AlignCenter)

            card_layout.addWidget(station)
            card_layout.addWidget(count)

            card.setLayout(card_layout)

            left.addWidget(card)

            self.station_labels.append(station)
            self.count_labels.append(count)

            # ---------- Performance Bar ----------
            bar_title = QLabel(f"Station {i+1}")
            bar_title.setFont(QFont("Arial",12))

            bar = QProgressBar()
            bar.setRange(0,100)

            bar.setStyleSheet(f"""
                QProgressBar {{
                    border:1px solid #888;
                    background:#444;
                    height:25px;
                    text-align:center;
                }}

                QProgressBar::chunk {{
                    background:{BAR_COLORS[i]};
                }}
            """)

            right.addWidget(bar_title)
            right.addWidget(bar)

            self.progress_bars.append(bar)

        content.addLayout(left,1)
        content.addLayout(right,1)

        main_layout.addLayout(content)

        self.setLayout(main_layout)

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_display)

        self.timer.start(1000)

        self.update_display()

    def update_display(self):

        try:

            with open(dashboard_file,"r") as f:
                data=json.load(f)

            counts=[s["count"] for s in data["stations"]]

            maximum=max(max(counts),1)

            for i,station in enumerate(data["stations"]):

                self.station_labels[i].setText(station["name"])

                self.count_labels[i].setText(str(station["count"]))

                percent=int((station["count"]/maximum)*100)

                self.progress_bars[i].setValue(percent)

        except Exception as e:

            print(e)


app=QApplication(sys.argv)

window=ProductionDashboard()

window.show()

sys.exit(app.exec())
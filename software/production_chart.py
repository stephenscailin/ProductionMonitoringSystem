import pyqtgraph as pg

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


STATION_COLORS = [
    "#FD7979",
    "#FFA77F",
    "#FFCC8F",
    "#7DC9FF",
    "#68A8F1",
    "#016180"
]


class ProductionChart(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()


        # -----------------------------
        # Graph Setup
        # -----------------------------

        self.graph = pg.PlotWidget()

        self.graph.setBackground(
            "#2B2B2B"
        )


        self.graph.setTitle(
            "PRODUCTION OUTPUT",
            color="#D0D0D0",
            size="16pt"
        )


        self.graph.showGrid(
            x=True,
            y=True,
            alpha=0.2
        )


        # Axis styling

        self.graph.getAxis(
            "bottom"
        ).setPen(
            QColor("#D0D0D0")
        )

        self.graph.getAxis(
            "left"
        ).setPen(
            QColor("#D0D0D0")
        )


        self.graph.getAxis(
            "bottom"
        ).setTextPen(
            QColor("#D0D0D0")
        )

        self.graph.getAxis(
            "left"
        ).setTextPen(
            QColor("#D0D0D0")
        )


        # X axis labels

        axis = self.graph.getAxis(
            "bottom"
        )

        axis.setTicks(
            [[
                (1, "1"),
                (2, "2"),
                (3, "3"),
                (4, "4"),
                (5, "5"),
                (6, "6")
            ]]
        )


        # X range

        self.graph.setXRange(
            0,
            7
        )


        # Y range

        self.graph.setYRange(
            0,
            100
        )


        # -----------------------------
        # Bars
        # -----------------------------

        self.bars = []


        for i in range(6):

            bar = pg.BarGraphItem(
                x=[i + 1],
                height=[0],
                width=0.6,
                brush=STATION_COLORS[i]
            )

            self.graph.addItem(
                bar
            )

            self.bars.append(
                bar
            )


        layout.addWidget(
            self.graph
        )


        # X-axis title

        x_label = QLabel(
            "Station"
        )

        x_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        x_label.setStyleSheet(
            """
            color:#D0D0D0;
            font-size:14px;
            """
        )


        layout.addWidget(
            x_label
        )


        self.setLayout(
            layout
        )


    def update_chart(self, stations):

        values = []


        for station in stations:

            values.append(
                station["count"]
            )


        if not values:
            return


        maximum = max(values)


        if maximum > 0:

            self.graph.setYRange(
                0,
                maximum * 1.2
            )


        for i, value in enumerate(values):

            self.bars[i].setOpts(
                height=[value]
            )
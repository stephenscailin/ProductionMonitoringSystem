from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class StationCard(QFrame):

    def __init__(self, name="Station", count=0, color="#FFFFFF"):

        super().__init__()

        self.setFixedHeight(95)


        self.setStyleSheet(f"""
    QFrame {{
        background-color:#555555;
        border-radius:12px;
        border:3px solid {color};
    }}

    QLabel {{
        color:white;
        background:transparent;
    }}
""")


        layout = QVBoxLayout()


        self.name = QLabel(name)

        self.name.setFont(
            QFont(
                "Segoe UI",
                11
            )
        )


        self.count = QLabel(str(count))

        self.count.setFont(
            QFont(
                "Segoe UI",
                24,
                QFont.Weight.Bold
            )
        )

        self.count.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        layout.addWidget(
            self.name
        )

        layout.addWidget(
            self.count
        )


        self.setLayout(
            layout
        )



    def update_data(self, station):

        self.name.setText(
            station["name"]
        )


        self.count.setText(
            str(station["count"])
        )


        # Change number color based on performance

        if station["status"] == "LOW OUTPUT":

            self.count.setStyleSheet(
                "color:#FD7979;"
            )

        else:

            self.count.setStyleSheet(
                "color:white;"
            )
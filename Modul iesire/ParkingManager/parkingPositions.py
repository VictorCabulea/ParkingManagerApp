from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from barrierWidget import BarrierWidget


class ParkingPositionsHandler(QWidget):
    def __init__(self):
        super(ParkingPositionsHandler, self).__init__()

        self.layout = QVBoxLayout()
        self.buttons = []

        self.vans_layout = QHBoxLayout()
        self.normal_cars_layout = QHBoxLayout()
        self.electric_cars_layout = QHBoxLayout()
        self.disabled_people_layout = QHBoxLayout()

        self.parking_map_layout = QHBoxLayout()

        self.row_1_parking = QVBoxLayout()
        self.row_2_parking = QVBoxLayout()
        self.row_3_parking = QVBoxLayout()
        self.row_4_parking = QVBoxLayout()
        self.row_5_parking = QVBoxLayout()
        self.row_6_parking = QVBoxLayout()
        self.row_7_parking = QVBoxLayout()
        self.row_8_parking = QVBoxLayout()

        self.barrier = BarrierWidget()

        self.setStyleSheet(open("resources/styles/styleParkingMap.txt").read())

        self.setup_position_buttons()

    def setup_position_buttons(self):
        rows = [self.row_1_parking, self.row_2_parking, self.row_3_parking, self.row_4_parking,
                self.row_5_parking, self.row_6_parking, self.row_7_parking, self.row_8_parking]
        row_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        for index in range(len(rows)):
            row = rows[index]
            label = row_labels[index]

            for i in range(0, 10):
                button = QPushButton(f"{label}{i + 1}")
                button.setObjectName(f"{label.lower()}_{i + 1}_position_button")
                button.setFixedSize(152, 70)

                self.buttons.append(button)

                row.addWidget(button)

            if index < 2:
                self.normal_cars_layout.addLayout(row)
                if index % 2 == 0:
                    self.normal_cars_layout.addSpacing(-5)
            elif index < 4:
                self.vans_layout.addLayout(row)
                if index % 2 == 0:
                    self.vans_layout.addSpacing(-5)
            elif index < 6:
                self.electric_cars_layout.addLayout(row)
                if index % 2 == 0:
                    self.electric_cars_layout.addSpacing(-5)
            elif index >= 6:
                self.disabled_people_layout.addLayout(row)
                if index % 2 == 0:
                    self.disabled_people_layout.addSpacing(-5)

        self.parking_map_layout.addSpacing(-20)
        self.parking_map_layout.addLayout(self.normal_cars_layout)
        self.parking_map_layout.addLayout(self.vans_layout)
        self.parking_map_layout.addLayout(self.electric_cars_layout)
        self.parking_map_layout.addLayout(self.disabled_people_layout)

        self.layout.addLayout(self.parking_map_layout)

        self.setLayout(self.layout)

    def get_button(self, button_id):
        random_button = self.buttons[button_id]
        return random_button

    def get_buttons(self):
        return self.buttons

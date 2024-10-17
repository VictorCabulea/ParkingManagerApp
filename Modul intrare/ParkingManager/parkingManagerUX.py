from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QFrame, QPushButton, QHBoxLayout, QVBoxLayout, \
    QDesktopWidget

from barrierWidget import BarrierWidget
from handler import Handler


class ParkingManagerUX(QWidget):
    def __init__(self):
        super(ParkingManagerUX, self).__init__()

        self.parking_places_available_label = QLabel()
        self.handler = Handler(self.parking_places_available_label)

        self.layout = QHBoxLayout()

        self.parking_management_layout = QVBoxLayout()
        self.choosing_vehicle_type_buttons_layout = QHBoxLayout()
        self.barrier_places_remaining_and_statistics_layout = QHBoxLayout()
        self.parking_plan_layout = QVBoxLayout()

        self.camera_label = QLabel(self)

        self.select_type_of_vehicle_label = QLabel("\t\tSelect the type of vehicle:")

        self.vans_and_bigger_cars_button = QPushButton()
        self.normal_cars_button = QPushButton()
        self.electric_cars_button = QPushButton()
        self.disabled_people_cars_button = QPushButton()

        self.statistics_button = QPushButton("Statistics")
        self.statistics_button.setObjectName("statistics_button")

        self.info_text = QTextEdit()
        self.line = QFrame()

        self.barrier = BarrierWidget()
        self.barrier_timer = QTimer()

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("License Plate Recognition")
        self.resize_to_screen()

        self.setup_other_widgets()
        self.set_widgets_for_choosing_type_of_vehicle()

        self.add_widgets_to_the_layouts()

        self.setup_style()

    def resize_to_screen(self):
        screen_resolution = QDesktopWidget().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        self.resize(width, height)

    def set_widgets_for_choosing_type_of_vehicle(self):
        self.vans_and_bigger_cars_button.setText("Vans and Bigger \nCars")
        self.normal_cars_button.setText("Normal \nCars")
        self.electric_cars_button.setText("Electric \nCars")
        self.disabled_people_cars_button.setText("Disabled People \nCars")

        self.select_type_of_vehicle_label.setObjectName("select_type_of_vehicle_label")

        self.vans_and_bigger_cars_button.setObjectName("vans_and_bigger_cars_button")
        self.normal_cars_button.setObjectName("normal_cars_button")
        self.electric_cars_button.setObjectName("electric_cars_button")
        self.disabled_people_cars_button.setObjectName("disabled_people_cars_button")

        self.choosing_vehicle_type_buttons_layout.addWidget(self.vans_and_bigger_cars_button)
        self.choosing_vehicle_type_buttons_layout.addWidget(self.normal_cars_button)
        self.choosing_vehicle_type_buttons_layout.addWidget(self.electric_cars_button)
        self.choosing_vehicle_type_buttons_layout.addWidget(self.disabled_people_cars_button)

    def setup_other_widgets(self):
        self.camera_label.setObjectName("camera_label")

        self.info_text.setReadOnly(True)
        self.info_text.setObjectName("info_text")

        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.parking_places_available_label.setObjectName("parking_places_available_label")

        self.barrier_timer.setSingleShot(True)

    def add_widgets_to_the_layouts(self):
        self.parking_management_layout.addWidget(self.statistics_button)
        self.parking_management_layout.addWidget(self.camera_label)
        self.parking_management_layout.addWidget(self.select_type_of_vehicle_label)
        self.parking_management_layout.addLayout(self.choosing_vehicle_type_buttons_layout)
        self.parking_management_layout.addWidget(self.info_text)

        self.barrier_places_remaining_and_statistics_layout.addSpacing(300)
        self.barrier_places_remaining_and_statistics_layout.addWidget(self.handler.get_barrier())
        self.barrier_places_remaining_and_statistics_layout.addSpacing(160)
        self.barrier_places_remaining_and_statistics_layout.addWidget(self.parking_places_available_label)
        self.barrier_places_remaining_and_statistics_layout.addSpacing(160)

        self.parking_plan_layout.addLayout(self.barrier_places_remaining_and_statistics_layout)

        self.parking_plan_layout.addWidget(self.handler.get_parking_positions_handler())

        self.layout.addLayout(self.parking_management_layout)
        self.layout.addWidget(self.line)
        self.layout.addLayout(self.parking_plan_layout)

        self.setLayout(self.layout)

    def setup_style(self):
        self.setStyleSheet(open("resources/styles/style.txt").read())

        self.camera_label.setFixedSize(580, 480)
        self.info_text.setMaximumWidth(580)


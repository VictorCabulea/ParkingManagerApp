from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from ledWidget import LEDWidget


class BarrierWidget(QWidget):
    def __init__(self, parent=None):
        super(BarrierWidget, self).__init__(parent)
        self.image_label = QLabel()

        self.barrier_open_pixmap = QPixmap("resources/images/barrier_open.png").scaled(100, 100, Qt.KeepAspectRatio)
        self.barrier_closed_pixmap = QPixmap("resources/images/barrier_closed.png").scaled(100, 100, Qt.KeepAspectRatio)

        self.led_indicator = LEDWidget()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.led_indicator)
        self.layout.addWidget(self.image_label)

        self.setup_barrier()
        self.setLayout(self.layout)

    def setup_barrier(self):
        self.image_label.setPixmap(self.barrier_closed_pixmap)
        self.image_label.setScaledContents(True)

    def close_barrier(self):
        self.image_label.setPixmap(self.barrier_closed_pixmap)
        self.image_label.setScaledContents(True)

        self.led_indicator.toggle_to_red()

    def open_barrier(self):
        self.image_label.setPixmap(self.barrier_open_pixmap)
        self.image_label.setScaledContents(True)

        self.led_indicator.toggle_to_green()

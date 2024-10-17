from PyQt5.QtWidgets import QWidget, QLabel


class LEDWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.label.setGeometry(0, 0, 20, 20)
        self.label.setStyleSheet('background-color: red; border-radius: 10px;')

    def toggle_to_green(self):
        self.label.setStyleSheet('background-color: green; border-radius: 10px;')

    def toggle_to_red(self):
        self.label.setStyleSheet('background-color: red; border-radius: 10px;')

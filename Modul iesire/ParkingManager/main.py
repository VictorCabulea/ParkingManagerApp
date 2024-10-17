from PyQt5.QtWidgets import QApplication
from parkingManager import ParkingManager

if __name__ == '__main__':
    app = QApplication([])
    window = ParkingManager()
    app.exec_()

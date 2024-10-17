import threading
import time
from datetime import datetime
from otherFunctions import *
from parkingManagerUX import ParkingManagerUX
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QLabel, QDialog
from PyQt5.QtCore import QTimer, pyqtSlot, pyqtSignal, Qt
import matplotlib.pyplot as plt
import tempfile
import numpy as np

BASE_URL = "http://192.168.100.22:8000/api/parking_service"


class ParkingManager(ParkingManagerUX):
    update_camera_signal = pyqtSignal(QPixmap)
    correct_number_detected_signal = pyqtSignal()

    def __init__(self):
        super(ParkingManager, self).__init__()
        self.barrier_opened = False
        self.cap = initialize_camera()
        self.running = True
        self.capture_thread = threading.Thread(target=self.capture_and_detect)
        self.capture_thread.daemon = True

        self.plate_number = None
        self.vehicle_type = None

        self.connect_widgets()
        self.setup_message_boxes_for_each_parking_lot()
        self.show()

        self.update_camera_signal.connect(self.update_camera_label)
        self.correct_number_detected_signal.connect(self.correct_number_detected)
        self.capture_thread.start()

        self.parking_update_thread = threading.Thread(target=self.update_parking_status_periodically)
        self.parking_update_thread.daemon = True
        self.parking_update_thread.start()

    def capture_and_detect(self):
        while self.running:
            try:
                ret, frame = self.cap.read()
                if ret:
                    detection = self.handler.get_plate_number_detector_handler().validate_number(frame)
                    if not self.barrier_opened and detection[0]:
                        self.plate_number = detection[1]
                        # Emit the signal instead of calling the method directly
                        self.correct_number_detected_signal.emit()
                        qImage = convert_to_qImage(detection[2])
                        self.update_camera_signal.emit(QPixmap.fromImage(qImage))
                    else:
                        qImage = convert_to_qImage(detection[2])
                        self.update_camera_signal.emit(QPixmap.fromImage(qImage))
            except Exception as e:
                print(f"Unhandled exception in capture_and_detect: {e}")

    def update_parking_status_periodically(self):
        while self.running:
            self.handler.complete_parking_map()
            time.sleep(15)

    @pyqtSlot()
    def correct_number_detected(self):
        current_date = datetime.now()

        occupied_by = self.plate_number
        response = requests.get(f"{BASE_URL}/parkingPlace/occupied_by/{occupied_by}")

        if response.status_code == 200:
            parkingPlace = response.json()['parkingPlace']
            print(parkingPlace)
            self.car_leaves_parking_zone(parkingPlace['parking_place_id'], occupied_by)
        else:
            self.info_text.setText(self.info_text.toPlainText() + "\n" +
                                       str(current_date.strftime("%H:%M:%S"))
                                       + f" -> Car '{self.plate_number}' - "
                                         f"No such car was found in the parking zone!")
            self.handler.sound_manager.play_sound("masina_nu_e_in_parcare")

    @pyqtSlot(QPixmap)
    def update_camera_label(self, qPixmap):
        self.camera_label.setPixmap(qPixmap)

    def closeEvent(self, event):
        self.running = False
        self.capture_thread.join()
        if self.cap.isOpened():
            self.cap.release()
        super().closeEvent(event)

    def connect_widgets(self):
        self.statistics_button.clicked.connect(self.show_statistics)

        self.barrier_timer.timeout.connect(self.close_barrier)

    def allow_car_to_leave_parking_zone(self, parking_place_id: str):
        index = 0

        if parking_place_id[0] == "A":
            numeric_part = parking_place_id[1:]
            index = int(numeric_part) - 1
        elif parking_place_id[0] == "B":
            numeric_part = parking_place_id[1:]
            index = int(numeric_part) + 10 - 1
        elif parking_place_id[0] == "C":
            numeric_part = parking_place_id[1:]
            index = int(numeric_part) + 20 - 1
        elif parking_place_id[0] == "D":
            numeric_part = parking_place_id[1:]
            index = int(numeric_part) + 30 - 1
        elif parking_place_id[0] == "E":
            numeric_part = parking_place_id[1:]
            index = int(numeric_part) + 40 - 1
        elif parking_place_id[0] == "F":
            numeric_part = parking_place_id[1:]
            index = int(numeric_part) + 50 - 1
        elif parking_place_id[0] == "G":
            numeric_part = parking_place_id[1:]
            index = int(numeric_part) + 60 - 1
        elif parking_place_id[0] == "H":
            numeric_part = parking_place_id[1:]
            index = int(numeric_part) + 70 - 1

        button = self.handler.get_parking_positions_handler().get_button(index)
        button.setStyleSheet("color: rgb(0, 0, 0)")
        reset_button_text(button, index)

        self.info_text.setText(self.info_text.toPlainText() + "\n" + str(datetime.now().strftime("%H:%M:%S"))
                               + f" -> Car {self.plate_number} - has left the parking zone.")
        self.handler.complete_parking_map()

        self.handler.sound_manager.play_sound("parasiti_parcarea")
        self.open_barrier()

    def car_leaves_parking_zone(self, parking_place_id: str, plate_number: str):
        response_payment = requests.get(f"{BASE_URL}/payment/plate_number/{plate_number}")
        if response_payment.status_code == 200:
            payment = response_payment.json()
            payment_date = datetime.strptime(payment['payment']['payment_date'], "%Y-%m-%dT%H:%M:%S")
            self.payment_label.setStyleSheet("background-color: green;")
            self.payment_label.setText("Payment Info: " + str(payment['payment']['price']) + " LEI at " + str(payment_date))

            time_difference = (datetime.now() - payment_date).total_seconds()
            if time_difference < 300:
                url = f"{BASE_URL}/parkingPlace/parking_place_id/{parking_place_id}"
                payload = {"occupied_by": plate_number}
                response = requests.patch(url, json=payload)

                if response.status_code == 204:
                    self.allow_car_to_leave_parking_zone(parking_place_id)

                    response_parkedCar = requests.delete(f"{BASE_URL}/parkedCar/plate_number/{plate_number}")
                    if response_parkedCar.status_code == 204:
                        print("Car left the parking zone successfully.")
                else:
                    print("Failed to update parking place. Error code:", response.status_code)
            else:
                self.payment_label.setStyleSheet("background-color: red;")
                self.info_text.setText(self.info_text.toPlainText() + "\n" + str(datetime.now().strftime("%H:%M:%S"))
                                       + f" -> Payment for Car {plate_number} is not longer valid.")
                self.handler.sound_manager.play_sound("plata_invalida")
        else:
            print("Failed to fetch payment. Error code:", response_payment.status_code)

            self.info_text.setText(self.info_text.toPlainText() + "\n" + str(datetime.now().strftime("%H:%M:%S"))
                                   + f" -> There is no payment for Car {plate_number}.")
            self.handler.sound_manager.play_sound("plata_inexistenta")

        self.plate_number = None
        self.vehicle_type = None

    def open_barrier(self):
        self.handler.get_barrier().open_barrier()
        self.barrier_opened = True
        self.barrier_timer.start(10000)

    def close_barrier(self):
        self.info_text.setText(self.info_text.toPlainText() + "\n" + str(datetime.now().strftime("%H:%M:%S"))
                               + " -> Gate closed, waiting for the next car...")
        self.handler.get_barrier().close_barrier()
        self.barrier_opened = False

    def set_vehicle_type_vans(self):
        self.vehicle_type = 1
        self.correct_number_detected()

    def set_vehicle_type_normal(self):
        self.vehicle_type = 2
        self.correct_number_detected()

    def set_vehicle_type_electric(self):
        self.vehicle_type = 3
        self.correct_number_detected()

    def set_vehicle_type_disabled(self):
        self.vehicle_type = 4
        self.correct_number_detected()

    def setup_message_boxes_for_each_parking_lot(self):
        buttons = self.handler.get_parking_positions_handler().get_buttons()

        for button in buttons:
            button.clicked.connect(lambda checked, b=button: self.show_message(b))

    def show_statistics(self):
        response = requests.get(f"{BASE_URL}/payments")
        if response.status_code == 200:
            payments = response.json().get("payments", [])

            total_money = 0
            vehicle_type_counts = {}

            for payment in payments:
                total_money += payment.get("price", 0)
                vehicle_type = payment.get("type_of_vehicle", "Unknown")
                if vehicle_type in vehicle_type_counts:
                    vehicle_type_counts[vehicle_type] += 1
                else:
                    vehicle_type_counts[vehicle_type] = 1

            # Define a fixed mapping of vehicle types to colors
            color_map = {
                1: 'red',
                2: 'yellow',
                3: 'green',
                4: 'blue'
            }

            # Create a temporary file to save the plot image
            temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            temp_file.close()

            # Plot the bar chart for vehicle type counts
            vehicle_types = list(vehicle_type_counts.keys())
            counts = list(vehicle_type_counts.values())
            colors = [color_map[vehicle_type] for vehicle_type in vehicle_types]

            plt.figure(figsize=(10, 6))
            bars = plt.bar(vehicle_types, counts, color=colors)
            plt.xlabel('Type of Vehicle')
            plt.ylabel('Number of Payments')
            plt.title('Number of Payments for Each Type of Vehicle')
            plt.xticks(vehicle_types)
            plt.grid(True, axis='y')
            plt.yticks(np.arange(1, max(counts) + 1, step=1))

            # Save the plot to the temporary file
            plt.savefig(temp_file.name)
            plt.close()

            # Create a dialog to display the image
            dialog = QDialog(self)
            dialog.setWindowTitle("Payment Statistics")

            layout = QVBoxLayout()

            label = QLabel()
            pixmap = QPixmap(temp_file.name)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)

            layout.addWidget(label)

            rounded_total_money = round(total_money, 2)
            message = f"There have been {len(payments)} payments recorded.\n" \
                      f"Total money generated: {rounded_total_money} LEI.\n"
            message_label = QLabel(message)
            message_label.setAlignment(Qt.AlignCenter)
            message_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
            layout.addWidget(message_label)

            dialog.setLayout(layout)
            dialog.exec_()


    def show_message(self, button):
        button_text_length = len(button.text())
        if button_text_length <= 3:
            QMessageBox.information(self, "Button Clicked",
                                    f"The place {button.text()} is empty and can be rented!")
        else:
            response = requests.get(f"{BASE_URL}/parkedCar/plate_number/{button.text()}")
            if response.status_code == 200:
                parkedCar = response.json()['parkedCar']
                type_of_vehicle_text = ""
                if parkedCar['type_of_vehicle'] == 1:
                    type_of_vehicle_text = "a Van/Bigger Car"
                elif parkedCar['type_of_vehicle'] == 2:
                    type_of_vehicle_text = "a Normal Car"
                elif parkedCar['type_of_vehicle'] == 3:
                    type_of_vehicle_text = "an Electric Car"
                elif parkedCar['type_of_vehicle'] == 4:
                    type_of_vehicle_text = "a Disabled Car"

                QMessageBox.information(self, "Button Clicked",
                                        f"This place is occupied by the car with the plate number {parkedCar['plate_number']}.\n"
                                        f"The car has been parked since {parkedCar['entry_time']}.\n"
                                        f"The car is {type_of_vehicle_text} "
                                        f"and it pays {parkedCar['price_per_hour']} LEI/hour.\n")


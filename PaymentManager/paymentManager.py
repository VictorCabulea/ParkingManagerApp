from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QSizePolicy
from DTO.paymentDTO import PaymentDTO
import requests
from paymentValidation import *
from plateNumberValidation import *

BASE_URL = "http://192.168.100.22:8000"


class PaymentWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.price = 0
        self.VALID_ROMANIAN_REGIONS = read_valid_regions()
        self.setWindowTitle("Payment Machine")
        self.setup_ui()

        self.resize(400, 800)

        self.setStyleSheet(open("resources/style/style.txt").read())

    def setup_ui(self):
        layout = QVBoxLayout()

        self.price = 0
        self.type_of_vehicle = 0

        self.plate_number_input = QLineEdit()
        layout.addWidget(QLabel("Plate Number (ex: RO IS 78 MON)"))
        layout.addWidget(self.plate_number_input)

        self.email_input = QLineEdit()
        layout.addWidget(QLabel("Email address (not mandatory)"))
        layout.addWidget(self.email_input)

        self.search_button = QPushButton("Search for Vehicle")
        self.search_button.clicked.connect(self.search_and_update_price_for_vehicle)
        layout.addWidget(self.search_button)

        self.entry_time_label = QLabel("Entry Date:")
        layout.addWidget(self.entry_time_label)

        self.payment_date_label = QLabel("Payment Date:")
        layout.addWidget(self.payment_date_label)

        self.time_difference_label = QLabel("Time Difference:")
        layout.addWidget(self.time_difference_label)

        self.vehicle_type_label = QLabel("Vehicle Type:")
        layout.addWidget(self.vehicle_type_label)

        self.price_per_hour_label = QLabel("Price/Hour:")
        layout.addWidget(self.price_per_hour_label)

        self.amount_label = QLabel("Amount:")
        layout.addWidget(self.amount_label)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.card_number = QLineEdit()
        layout.addWidget(QLabel("Card Number (xxxx xxxx xxxx xxxx)"))
        layout.addWidget(self.card_number)

        self.expiry_date = QLineEdit()
        layout.addWidget(QLabel("Expiry Date (MM/YY)"))
        layout.addWidget(self.expiry_date)

        self.cvc = QLineEdit()
        layout.addWidget(QLabel("CVC (xyz)"))
        layout.addWidget(self.cvc)

        self.pay_button = QPushButton("Pay!")
        self.pay_button.setEnabled(False)
        self.pay_button.clicked.connect(self.create_payment)
        layout.addWidget(self.pay_button)

        self.payment_information = QLabel("Payment Information: ")
        layout.addWidget(self.payment_information)

        self.setLayout(layout)

    def search_and_update_price_for_vehicle(self):
        plate_number = self.plate_number_input.text()

        if validate_number(plate_number, self.VALID_ROMANIAN_REGIONS):
            try:
                response = requests.get(f"{BASE_URL}/api/parking_service/parkedCar/plate_number/{plate_number}")
                response.raise_for_status()

                vehicle_data = response.json().get('parkedCar', {})
                self.type_of_vehicle = vehicle_data.get('type_of_vehicle')
                price_per_hour = vehicle_data.get('price_per_hour')
                entry_time_str = vehicle_data.get('entry_time')

                if not self.type_of_vehicle or not price_per_hour or not entry_time_str:
                    raise ValueError("Incomplete vehicle information.")

                payment_date = datetime.now()
                formatted_payment_date = payment_date.strftime("%Y-%m-%dT%H:%M:%S")

                try:
                    response_payment = requests.get(
                        f"{BASE_URL}/api/parking_service/payment/plate_number/{plate_number}")
                    response_payment.raise_for_status()

                    previous_payment_time_str = response_payment.json().get('payment', {}).get('payment_date')
                    previous_payment_time = datetime.fromisoformat(
                        previous_payment_time_str) if previous_payment_time_str else None
                except requests.RequestException:
                    previous_payment_time = None

                if previous_payment_time:
                    time_difference = (payment_date - previous_payment_time).total_seconds() / 3600
                    entry_time_display = previous_payment_time_str
                else:
                    entry_time = datetime.fromisoformat(entry_time_str)
                    time_difference = (payment_date - entry_time).total_seconds() / 3600
                    entry_time_display = entry_time_str

                time_difference_rounded = round(time_difference, 2)
                self.price = round((price_per_hour * time_difference_rounded),2)

                self.entry_time_label.setText("Entry Date: " + entry_time_display)
                self.payment_date_label.setText("Payment Date: " + formatted_payment_date)
                self.time_difference_label.setText("Time Difference: " + str(time_difference_rounded) + " hours")
                self.vehicle_type_label.setText("Vehicle Type: " + str(self.type_of_vehicle))
                self.price_per_hour_label.setText("Price/Hour: " + str(price_per_hour) + " LEI")
                self.amount_label.setText("Amount: " + str(self.price) + " LEI")

                self.search_button.setEnabled(False)
                self.pay_button.setEnabled(True)

            except requests.RequestException:
                self.payment_information.setText("Failed to retrieve vehicle information.")
            except ValueError as e:
                self.payment_information.setText(str(e))
        else:
            self.payment_information.setText("Invalid plate number!")


    def create_payment(self):
        if (not validate_card_number(self.card_number.text()) or not
                validate_expiry_date(self.expiry_date.text()) or not
                validate_cvc(self.cvc.text())):
            self.payment_information.setText("Invalid Input!")
            return

        try:
            response = requests.get(f"{BASE_URL}/api/parking_service/payments")
            if response.status_code == 200:
                payments_data = response.json()
                payments_length = len(payments_data['payments'])
            else:
                payments_length = 0
        except requests.RequestException as e:
            self.payment_information.setText("Error retrieving payments!")
            print(f"Error: {e}")
            return

        plate_number = self.plate_number_input.text()
        account_email = self.email_input.text()
        payment_date = datetime.now().isoformat()

        payment = PaymentDTO(
            payment_id=payments_length + 1,
            plate_number=plate_number,
            type_of_vehicle=self.type_of_vehicle,
            account_email=account_email,
            price=self.price,
            payment_date=payment_date
        )

        try:
            response = requests.post(f"{BASE_URL}/api/parking_service/payment", json=payment.dict())
            if response.status_code == 201:
                self.payment_information.setText("Payment Information: Success!")

                self.price = 0

                self.search_button.setEnabled(True)
                self.pay_button.setEnabled(False)
            else:
                self.payment_information.setText("Payment Information: Failed!")
        except requests.RequestException as e:
            self.payment_information.setText("Error making payment!")
            print(f"Error: {e}")

import requests
import cv2
import pygame
from PyQt5.QtGui import QColor, QImage

BASE_URL = "http://localhost:8000/api/parking_service"


def initialize_camera():
    try:
        cap = cv2.VideoCapture(0)
        return cap
    except Exception as e:
        print("Error occurred while initializing camera:", e)
        return None


def read_valid_regions():
    with open("resources/valid regions/valid_romanian_regions.txt", "r") as file:
        VALID_ROMANIAN_REGIONS = [line.strip() for line in file]

    return VALID_ROMANIAN_REGIONS


def toggle_button_color(button):
    current_color = button.palette().color(button.foregroundRole())
    if current_color == QColor(0, 0, 0):
        button.setStyleSheet("color: rgb(255, 255, 255)")
    else:
        button.setStyleSheet("color: rgb(0, 0, 0)")


def load_sound(sound_path):
    return pygame.mixer.Sound(sound_path)


def select_sound_based_on_available_parking_lot(parking_place_id):
    sound_name = parking_place_id

    return sound_name


def get_occupied_parking_places_and_set_parking_lots_available_label_text(label):
    cnt_empty_places = 0

    response = requests.get(f"{BASE_URL}/ParkingPlaces")
    if response.status_code == 200:
        parking_data = response.json()
        parking_place_id_list = []
        occupied_by_list = []
        parking_places = parking_data.get('ParkingPlaces', [])

        for parking_place in parking_places:
            parking_place_id = parking_place['parkingPlace'].get('parking_place_id')
            occupied_by = parking_place['parkingPlace'].get('occupied_by')

            parking_place_id_list.append(parking_place_id)

            if occupied_by is not None:
                first_space_index = occupied_by.find(' ')
                if first_space_index != -1:
                    occupied_by = occupied_by[:first_space_index] + '\n' + occupied_by[first_space_index + 1:]
                occupied_by_list.append(occupied_by)
            else:
                occupied_by_list.append("")
                cnt_empty_places += 1

        print(parking_place_id_list)
        print(occupied_by_list)

        label.setText(f"Available parking lots: {cnt_empty_places}/80")

        return parking_place_id_list, occupied_by_list
    else:
        print("Failed to fetch parking places. Error code:", response.status_code)
        return []


def convert_to_qImage(cvMatImage):
    image = cv2.cvtColor(cvMatImage, cv2.COLOR_BGR2RGB)
    h, w, ch = image.shape
    bytesPerLine = ch * w
    qImage = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)

    return qImage

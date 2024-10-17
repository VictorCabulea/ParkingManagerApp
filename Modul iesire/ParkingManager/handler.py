from barrierWidget import BarrierWidget
from otherFunctions import get_occupied_parking_places_and_set_parking_lots_available_label_text
from parkingPositions import ParkingPositionsHandler
from plateNumberDetector import PlateNumberDetectorHandler
from soundManager import SoundManager


class Handler:
    def __init__(self, label):
        self.label = label

        self.parking_positions_handler = ParkingPositionsHandler()
        self.plate_number_detector_handler = PlateNumberDetectorHandler()

        self.sound_manager = SoundManager()
        self.sound_manager.load_sounds()

        self.complete_parking_map()
        self.barrier = BarrierWidget()

    def complete_parking_map(self):
        parking_place_id_list, occupied_by_list = (
            get_occupied_parking_places_and_set_parking_lots_available_label_text(self.label))

        for i in range(0, len(self.parking_positions_handler.get_buttons())):
            index = 0
            if parking_place_id_list[i][0] == "A":
                numeric_part = parking_place_id_list[i][1:]
                index = int(numeric_part) - 1
            elif parking_place_id_list[i][0] == "B":
                numeric_part = parking_place_id_list[i][1:]
                index = int(numeric_part) + 10 - 1
            elif parking_place_id_list[i][0] == "C":
                numeric_part = parking_place_id_list[i][1:]
                index = int(numeric_part) + 20 - 1
            elif parking_place_id_list[i][0] == "D":
                numeric_part = parking_place_id_list[i][1:]
                index = int(numeric_part) + 30 - 1
            elif parking_place_id_list[i][0] == "E":
                numeric_part = parking_place_id_list[i][1:]
                index = int(numeric_part) + 40 - 1
            elif parking_place_id_list[i][0] == "F":
                numeric_part = parking_place_id_list[i][1:]
                index = int(numeric_part) + 50 - 1
            elif parking_place_id_list[i][0] == "G":
                numeric_part = parking_place_id_list[i][1:]
                index = int(numeric_part) + 60 - 1
            elif parking_place_id_list[i][0] == "H":
                numeric_part = parking_place_id_list[i][1:]
                index = int(numeric_part) + 70 - 1

            button = self.parking_positions_handler.get_button(index)

            if occupied_by_list[i] == "":
                button.setText(f"{parking_place_id_list[i][0]}{index%10+1}")
            else:
                button.setText(occupied_by_list[i])

    def get_parking_positions_handler(self):
        return self.parking_positions_handler

    def get_plate_number_detector_handler(self):
        return self.plate_number_detector_handler

    def get_barrier(self):
        return self.barrier

    def get_sound_manager(self):
        return self.sound_manager

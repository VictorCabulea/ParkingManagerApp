import numpy as np
from easyocr import easyocr
from collections import Counter

from otherFunctions import *


class PlateNumberDetectorHandler:
    def __init__(self):
        self.reader = easyocr.Reader(['en'])

        self.most_common_plate_number = ""
        self.detections = []

        self.VALID_ROMANIAN_REGIONS = read_valid_regions()

    def validate_number(self, frame):
        result = self.reader.readtext(frame)

        plate_info = []

        for res in result:
            if res[1].isalnum():
                plate_info.append(res[1].upper())
                pts = res[0]
                try:
                    cv2.polylines(frame, [np.array(pts)], isClosed=True, color=(0, 0, 255), thickness=3)
                except Exception as e:
                    print(f"An error occurred while adding a polyline: {e}")

        print(plate_info)
        if len(plate_info) == 4:
            if plate_info[0] == "RO":
                if plate_info[1] in self.VALID_ROMANIAN_REGIONS:
                    if plate_info[2].isdigit() and (plate_info[3].isalpha() and len(plate_info[3]) == 3):
                        self.detections.append(' '.join(plate_info))

        if len(self.detections) == 5:
            self.most_common_plate_number = Counter(self.detections).most_common(1)[0][0]
            self.detections = []
            return True, self.most_common_plate_number, frame
        else:
            return False, self.most_common_plate_number, frame

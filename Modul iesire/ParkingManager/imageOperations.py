import cv2
from PyQt5.QtGui import QImage


def convert_to_qImage(cvMatImage):
    image = cv2.cvtColor(cvMatImage, cv2.COLOR_BGR2RGB)
    h, w, ch = image.shape
    bytesPerLine = ch * w
    qImage = QImage(image.data, w, h, bytesPerLine, QImage.Format_RGB888)

    return qImage

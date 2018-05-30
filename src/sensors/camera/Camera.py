import cv2
from ..Sensor import Sensor

class Camera(Sensor):
    def __init__(port=0):
        self.camera = cv2.VideoCapture(port)

    def take_photo():
        raise NotImplementedError

    def send_to(server):
        raise NotImplementedError


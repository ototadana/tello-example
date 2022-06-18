import cv2

from info import Info
from startable import Startable


class DroneVideoReceiver(Startable):
    def start(self, info: Info) -> None:
        cap = cv2.VideoCapture("udp://0.0.0.0:11111?overrun_nonfatal=1")

        while info.is_active():
            success, image = cap.read()
            if not success:
                continue
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            info.set_image(image)

        cap.release()

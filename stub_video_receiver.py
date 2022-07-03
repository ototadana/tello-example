import cv2

from info import Info
from logger import get_logger
from startable import Startable


class StubVideoReceiver(Startable):
    device_id: int

    def __init__(self, device_id: int = 0) -> None:
        super().__init__()
        self.device_id = device_id

    def start(self, info: Info) -> None:
        logger = get_logger(__name__)
        logger.info("start")

        cap = cv2.VideoCapture(self.device_id)

        while info.is_active():
            success, image = cap.read()
            if not success:
                continue
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            info.set_image(image)

        cap.release()
        logger.info("done")

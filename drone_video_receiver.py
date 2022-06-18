import cv2


class DroneVideoReceiver:
    def start(self, info):
        cap = cv2.VideoCapture("udp://0.0.0.0:11111?overrun_nonfatal=1")

        while info.is_active():
            success, image = cap.read()
            if not success:
                continue
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            info.set_image(image)

        cap.release()

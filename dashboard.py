import cv2
import numpy as np
import PySimpleGUI as sg
from PIL import Image, ImageTk

from info import Info
from logger import get_logger
from runnable import Runnable


class Dashboard(Runnable):
    def run(self, info: Info) -> None:
        logger = get_logger(__name__)
        logger.info("start")

        DISPLAY_SIZE = (800, 600)
        layout = [
            [sg.Image(filename="", key="image", size=DISPLAY_SIZE)],
            [sg.Text("Command:"), sg.Input(), sg.Button("OK")],
            [
                sg.Text(key="sent", font=("monospace", 20)),
                sg.Text(text="-->"),
                sg.Text(key="recv", font=("monospace", 20)),
            ],
            [sg.Text(key="state", font=("monospace", 20))],
            [
                sg.Button("Quit", font=("Arial", 32)),
                sg.Button("Takeoff", font=("Arial", 32)),
                sg.Button("Land", font=("Arial", 32)),
            ],
        ]
        window = sg.Window("My Drone", layout)

        while True:
            msg = ""
            event, values = window.read(timeout=1)
            if event == sg.WINDOW_CLOSED or event == "Quit":
                break

            window["state"].update(f'battery: {info.get_state("bat"):.1f}%')

            image = info.get_image()
            if image is None:
                continue

            h, w, _ = np.shape(image)
            r = DISPLAY_SIZE[0] / w
            image = cv2.resize(image, (int(w * r), int(h * r)))
            photoImage = ImageTk.PhotoImage(Image.fromarray(image))
            window["image"].update(data=photoImage)

            if event == "OK":
                msg = values[0]
            if event == "Takeoff":
                msg = "takeoff"
            if event == "Land":
                msg = "land"

            if msg != "":
                info.entry_command(msg)

            window["sent"].update(info.get_sent_command())
            window["recv"].update(info.get_command_result())

        info.stop()
        window.close()
        logger.info("done")

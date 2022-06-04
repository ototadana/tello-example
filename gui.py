import random
import threading
import time

import PySimpleGUI as sg

layout = [
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


class Info:
    def __init__(self):
        self.__state = {}
        self.__is_active = True

    def set_states(self, states):
        self.__state = states

    def get_states(self):
        return self.__state

    def get_state(self, name):
        return self.__state.get(name, 0.0)

    def is_active(self):
        return self.__is_active

    def stop(self):
        self.__is_active = False


info = Info()


def receive_state():
    while info.is_active():
        time.sleep(1)
        try:
            info.set_states({"bat": random.random() * 100})
        except Exception:
            print("\nExit . . .\n")
            break


state_receive_thread = threading.Thread(target=receive_state)
state_receive_thread.start()

while True:
    msg = ""
    event, values = window.read(timeout=1)
    window["state"].update(f'battery: {info.get_state("bat"):.1f}%')

    if event == sg.WINDOW_CLOSED or event == "Quit":
        break
    if event == "OK":
        msg = values[0]
    if event == "Takeoff":
        msg = "takeoff"
    if event == "Land":
        msg = "land"

    if msg == "":
        continue

    window["sent"].update(msg)
    window["recv"].update("ok")

info.stop()
window.close()

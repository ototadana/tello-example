import socket
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


def __get_drone_state(data):
    s = data.decode(errors="replace")
    values = s.split(";")
    state = {}
    for v in values:
        kv = v.split(":")
        if len(kv) > 1:
            state[kv[0]] = float(kv[1])
    return state


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 8889))

sock.sendto("command".encode(), ("192.168.10.1", 8889))
sock.recvfrom(1024)

state_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
state_sock.bind(("", 8890))


def receive_state():
    while info.is_active():
        try:
            data, _ = state_sock.recvfrom(1024)
            info.set_states(__get_drone_state(data))
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

    sock.sendto(msg.encode(), ("192.168.10.1", 8889))
    window["sent"].update(msg)
    start = time.time()
    data, _ = sock.recvfrom(1024)
    window["recv"].update(f"{data.decode()} {time.time() - start:.1f}")


info.stop()
window.close()

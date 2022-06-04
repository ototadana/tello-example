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

while True:
    msg = ""
    event, values = window.read(timeout=1)
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

window.close()

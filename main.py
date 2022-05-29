import socket
import threading
import time


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
data, _ = state_sock.recvfrom(1024)
print()
print(f'battery: {__get_drone_state(data)["bat"]}%')
print()


def receive_state():
    while True:
        try:
            data, _ = state_sock.recvfrom(1024)
            print(f'battery: {__get_drone_state(data)["bat"]}%')
        except Exception:
            print("\nExit . . .\n")
            break


state_receive_thread = threading.Thread(target=receive_state)
state_receive_thread.start()


print("Tello Python3 Demo.")
print("Tello: takeoff land flip forward back left right")
print("       up down cw ccw speed speed?")
print("end -- quit demo.")


while True:
    try:
        msg = input("> ")

        if not msg:
            break

        if "end" in msg:
            print("...")
            sock.close()
            break

        sock.sendto(msg.encode(), ("192.168.10.1", 8889))
        start = time.time()

        data, _ = sock.recvfrom(1024)
        print(data.decode(), f"{time.time() - start:.1f}\n")
    except KeyboardInterrupt:
        print(" . . .")
        sock.close()
        break

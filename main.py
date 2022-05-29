import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 8889))

print("Tello Python3 Demo.")
print("Tello: command takeoff land flip forward back left right")
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

        data = msg.encode(encoding="utf-8")
        sent = sock.sendto(data, ("192.168.10.1", 8889))
        start = time.time()

        data, server = sock.recvfrom(1518)
        print(data.decode(encoding="utf-8"), f"{time.time() - start:.1f}")
    except KeyboardInterrupt:
        print(" . . .")
        sock.close()
        break

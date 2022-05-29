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

        sock.sendto(msg.encode(), ("192.168.10.1", 8889))
        start = time.time()

        data, _ = sock.recvfrom(1024)
        print(data.decode(), f"{time.time() - start:.1f}\n")
    except KeyboardInterrupt:
        print(" . . .")
        sock.close()
        break

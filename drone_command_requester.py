import socket
import time

from info import Info
from logger import get_logger
from startable import Startable


class DroneCommandRequester(Startable):
    def start(self, info: Info) -> None:
        logger = get_logger(__name__)
        logger.info("start")

        DRONE_ADDRESS = ("192.168.10.1", 8889)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", 8889))

        sock.sendto("command".encode(), DRONE_ADDRESS)
        sock.recvfrom(1024)
        sock.sendto("streamon".encode(), DRONE_ADDRESS)
        sock.recvfrom(1024)

        while info.is_active():
            time.sleep(0.1)
            msg = info.pick_command()
            if msg == "":
                continue

            sock.sendto(msg.encode(), DRONE_ADDRESS)
            info.set_command_result("")
            info.set_sent_command(msg)
            start = time.time()
            data, _ = sock.recvfrom(1024)
            info.set_command_result(f"{data.decode()} {time.time() - start:.1f}")

        logger.info("done")

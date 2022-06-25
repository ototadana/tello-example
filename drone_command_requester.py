from logging import Logger
import socket
import time

from info import Info
from logger import get_logger
from startable import Startable


class DroneCommandRequester(Startable):
    def start(self, info: Info) -> None:
        logger = get_logger(__name__)
        logger.info("start")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(10)
        sock.bind(("", 8889))

        self.__send(sock, "command", info, logger)
        self.__send(sock, "streamon", info, logger)

        while info.is_active():
            time.sleep(0.1)
            msg = info.pick_command()
            if msg == "":
                continue

            self.__send(sock, msg, info, logger)

        logger.info("done")

    def __send(self, sock: socket.socket, msg: str, info: Info, logger: Logger) -> None:
        try:
            sock.sendto(msg.encode(), ("192.168.10.1", 8889))
            info.set_sent_command(msg)
            start = time.time()
            data, _ = sock.recvfrom(1024)
            info.set_command_result(f"{data.decode()} {time.time() - start:.1f}")
        except Exception:
            logger.exception("communication error")

from __future__ import annotations
import socket

from info import Info
from logger import get_logger
from startable import Startable


class DroneStateReceiver(Startable):
    def start(self, info: Info) -> None:
        logger = get_logger(__name__)
        logger.info("start")

        state_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        state_sock.bind(("", 8890))

        while info.is_active():
            try:
                data, _ = state_sock.recvfrom(1024)
                info.set_states(self.__get_drone_state(data))
            except Exception:
                print("\nExit . . .\n")
                break

        logger.info("done")

    def __get_drone_state(self, data: bytes) -> dict[str, float]:
        s = data.decode(errors="replace")
        values = s.split(";")
        state = {}
        for v in values:
            kv = v.split(":")
            if len(kv) > 1:
                state[kv[0]] = float(kv[1])
        return state

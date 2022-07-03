from __future__ import annotations
import time

from info import Info
from logger import get_logger
from startable import Startable


class StubStateReceiver(Startable):
    def start(self, info: Info) -> None:
        logger = get_logger(__name__)
        logger.info("start")

        while info.is_active():
            time.sleep(5)
            info.set_states({"bat": 38.0})

        logger.info("done")

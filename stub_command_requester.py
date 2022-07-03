import time

from info import Info
from logger import get_logger
from startable import Startable


class StubCommandRequester(Startable):
    def start(self, info: Info) -> None:
        logger = get_logger(__name__)
        logger.info("start")

        while info.is_active():
            time.sleep(0.1)
            msg = info.pick_command()
            if msg == "":
                continue

            info.set_sent_command(msg)
            time.sleep(1)
            info.set_command_result("OK")

        logger.info("done")

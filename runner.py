from __future__ import annotations

from threading import Thread

from info import Info
from runnable import Runnable
from startable import Startable


class Runner:
    def run(self, startables: list[Startable], runnable: Runnable) -> None:
        info = Info()

        for startable in startables:
            Thread(target=startable.start, args=(info,)).start()

        runnable.run(info)

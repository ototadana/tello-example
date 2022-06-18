from threading import Thread

from info import Info


class Runner:
    def run(self, startables, runnable):
        info = Info()

        for startable in startables:
            Thread(target=startable.start, args=(info,)).start()

        runnable.run(info)

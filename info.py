from __future__ import annotations

from cv2 import Mat


class Info:
    __state: dict[str, float]
    __is_active: bool
    __image: Mat
    __command: str
    __sent_command: str
    __result: str

    def __init__(self) -> None:
        self.__state = {}
        self.__is_active = True
        self.__image = None
        self.__command = ""
        self.__sent_command = ""
        self.__result = ""

    def set_states(self, states: dict[str, float]) -> None:
        self.__state = states

    def get_states(self) -> dict[str, float]:
        return self.__state

    def get_state(self, name: str) -> float:
        return self.__state.get(name, 0.0)

    def is_active(self) -> bool:
        return self.__is_active

    def stop(self) -> None:
        self.__is_active = False

    def set_image(self, image: Mat) -> None:
        self.__image = image

    def get_image(self) -> Mat:
        return self.__image

    def entry_command(self, command: str) -> None:
        self.__command = command

    def pick_command(self) -> str:
        command = self.__command
        self.__command = ""
        return command

    def set_sent_command(self, command: str) -> None:
        self.__sent_command = command

    def get_sent_command(self) -> str:
        return self.__sent_command

    def set_command_result(self, result: str) -> None:
        self.__result = result

    def get_command_result(self) -> str:
        return self.__result

from __future__ import annotations

from typing import Sequence

import mediapipe as mp

from info import Info
from logger import get_logger
from startable import Startable

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


class Landmark:
    x: float
    y: float
    z: float


class HandSensor(Startable):
    def start(self, info: Info) -> None:
        logger = get_logger(__name__)
        logger.info("start")

        with mp_hands.Hands(model_complexity=0) as hands:
            while info.is_active():
                image = info.get_image()
                if image is None:
                    continue

                results = hands.process(image)
                command = self.__get_command(results.multi_hand_landmarks)
                info.entry_command(command)

        logger.info("done")

    def __get_command(self, multi_hand_landmarks: list) -> str:
        if multi_hand_landmarks:
            for hand_landmarks in multi_hand_landmarks:
                command = self.__get_command_by_hand(hand_landmarks.landmark)
                if command != "":
                    return command
        return ""

    def __get_command_by_hand(self, hlm: Sequence[Landmark]) -> str:
        if self.__is_up(hlm):
            return "up 20"
        if self.__is_down(hlm):
            return "down 20"
        if self.__is_left(hlm):
            return "left 20"
        if self.__is_right(hlm):
            return "right 20"
        return ""

    def __is_up(self, hlm: Sequence[Landmark]) -> bool:
        if not (hlm[8].y < hlm[7].y < hlm[6].y < hlm[5].y < hlm[0].y):
            return False
        if hlm[12].y < hlm[11].y < hlm[10].y < hlm[0].y:
            return False
        if hlm[16].y < hlm[15].y < hlm[14].y < hlm[0].y:
            return False
        if hlm[20].y < hlm[19].y < hlm[18].y < hlm[0].y:
            return False
        return True

    def __is_down(self, hlm: Sequence[Landmark]) -> bool:
        if not (hlm[8].y > hlm[7].y > hlm[6].y > hlm[5].y > hlm[0].y):
            return False
        if hlm[12].y > hlm[11].y > hlm[10].y > hlm[0].y:
            return False
        if hlm[16].y > hlm[15].y > hlm[14].y > hlm[0].y:
            return False
        if hlm[20].y > hlm[19].y > hlm[18].y > hlm[0].y:
            return False
        return True

    def __is_left(self, hlm: Sequence[Landmark]) -> bool:
        if not (hlm[8].x < hlm[7].x < hlm[6].x < hlm[5].x < hlm[0].x):
            return False
        if hlm[12].x < hlm[11].x < hlm[10].x < hlm[0].x:
            return False
        if hlm[16].x < hlm[15].x < hlm[14].x < hlm[0].x:
            return False
        if hlm[20].x < hlm[19].x < hlm[18].x < hlm[0].x:
            return False
        return True

    def __is_right(self, hlm: Sequence[Landmark]) -> bool:
        if not (hlm[8].x > hlm[7].x > hlm[6].x > hlm[5].x > hlm[0].x):
            return False
        if hlm[12].x > hlm[11].x > hlm[10].x > hlm[0].x:
            return False
        if hlm[16].x > hlm[15].x > hlm[14].x > hlm[0].x:
            return False
        if hlm[20].x > hlm[19].x > hlm[18].x > hlm[0].x:
            return False
        return True

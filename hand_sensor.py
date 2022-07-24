from __future__ import annotations

from typing import Sequence

import mediapipe as mp
import numpy as np

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
                command = self.__get_command(
                    results.multi_hand_landmarks, results.multi_handedness
                )
                info.entry_command(command)

        logger.info("done")

    def __get_command(self, multi_hand_landmarks: list, multi_handedness: list) -> str:
        if multi_hand_landmarks:
            for i, hand_landmarks in enumerate(multi_hand_landmarks, 0):
                left_hand = multi_handedness[i].classification[0].label == "Left"
                command = self.__get_command_by_hand(hand_landmarks.landmark, left_hand)
                if command != "":
                    return command
        return ""

    def __get_command_by_hand(self, hlm: Sequence[Landmark], left_hand: bool) -> str:
        if self.__is_four_up(hlm):
            return self.__get_forward_or_back(hlm, left_hand)

        return self.__get_direction(hlm)

    def __is_four_up(self, hlm: Sequence[Landmark]) -> bool:
        if not (hlm[8].y < hlm[7].y < hlm[6].y < hlm[5].y < hlm[0].y):
            return False
        if not (hlm[12].y < hlm[11].y < hlm[10].y < hlm[0].y):
            return False
        if not (hlm[16].y < hlm[15].y < hlm[14].y < hlm[0].y):
            return False
        if not (hlm[20].y < hlm[19].y < hlm[18].y < hlm[0].y):
            return False
        return True

    def __get_forward_or_back(self, hlm: Sequence[Landmark], left_hand: bool) -> str:
        distance = hlm[8].x - hlm[20].x
        if distance < 0.05 and distance > -0.05:
            return ""

        if distance < 0:
            return "forward 20" if left_hand else "back 20"
        else:
            return "back 20" if left_hand else "forward 20"

    def __get_direction(self, hlm: Sequence[Landmark]) -> str:
        a = self.__angle(hlm[5], hlm[6], hlm[8])

        if self.__is_up(hlm) and a > 60 and a < 120:
            return "up 20"
        if self.__is_down(hlm) and a > 60 and a < 120:
            return "down 20"
        if self.__is_left(hlm) and a > 150:
            return "left 20"
        if self.__is_right(hlm) and a < 30:
            return "right 20"
        return ""

    def __angle(self, la: Landmark, lb: Landmark, lc: Landmark) -> float:
        a = np.array([la.x, la.y])
        b = np.array([lb.x, lb.y])
        c = np.array([lc.z, lc.y])
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        return np.degrees(angle)

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

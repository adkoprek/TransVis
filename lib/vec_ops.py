#  _______               __      ___     
# |__   __|              \ \    / (_)    
#    | |_ __ __ _ _ __  __\ \  / / _ ___ 
#    | | '__/ _` | '_ \/ __\ \/ / | / __|
#    | | | | (_| | | | \__ \\  /  | \__ \
#    |_|_|  \__,_|_| |_|___/ \/   |_|___/
#   https://git.psi.ch/hipa_apps/TransVis
#
# Implements a transformable vector which 
# automatically calculates its vector tip.
#
# @Author: Adam Koprek

import numpy as np
from copy import copy
from typing import Callable

from lib.line_ops import TransLine
from lib.line_ops import BEZS, PNTS


class TransTip:
    side: int

    # Creates the tip and calculates the initial tip with the given side lenght
    # perpendicular to the end of the provided line
    def __init__(self, line: TransLine, side: int) -> None:
        self.side = side
        self.vertecies = self._tip_vertecies_from_beizer(line.get_bezier(), self.side)
        self.trans_vertecies = np.array([])

    # Calculates the transformed vectercies using the side lenght passed in the
    # constuctor perpendicular to the end of the provided transfomed line
    def transform(self, line: TransLine) -> None:
        self.trans_vertecies = self._tip_vertecies_from_beizer(line.get_transform_bez(), self.side)

    # Returns the initial tip
    def get_tip(self) -> PNTS:
        return self.vertecies

    # Returns the transformed tip
    def get_trans_tip(self) -> PNTS:
        return self.trans_vertecies

    # This function takes the coefficient of a bezier curve and
    # creates the vertecies of an arrow tip sits on the tangent 
    # of the last two control points with side length l and reduces
    # the length of the line by l
    @staticmethod
    def _tip_vertecies_from_beizer(bezier: BEZS, l: int) -> PNTS:
        _, _, p3, p4 = copy(bezier[0])

        h = ((3 ** 0.5) * l) / 2
        tangent = p4 - p3
        tangent_length = (tangent[0] ** 2 + tangent[1] ** 2) ** 0.5
        tangent_proportion = h / tangent_length

        v1 = p4 + tangent * tangent_proportion

        ortho = np.array([tangent[1], -tangent[0]])
        ortho_length = (ortho[0] ** 2 + ortho[1] ** 2) ** 0.5
        ortho_prop = (l / 2) / ortho_length

        v2 = p4 + ortho_prop * ortho
        v3 = p4 - ortho_prop * ortho

        return np.array([v1, v2, v3])


class TransVector:
    line: TransLine
    tip: TransTip

    # Creates the vector which is build from a line and a tip
    def __init__(self, begin_x: float, end_x: float, begin_y: float, end_y: float, w: int) -> None:
        self.line = TransLine(begin_x, end_x, begin_y, end_y, 1)
        self.tip = TransTip(self.line, w)

    # Transforms the vector using the given functions
    def transform(self, xt: Callable[[float, float], float], yt: Callable[[float, float], float]) -> None:
        self.line.transform(xt, yt)
        self.tip.transform(self.line)

    # Scales the entire vector 
    def scale(self, s: float) -> None:
        self.line.scale_transformed(s)
        self.tip.transform(self.line)

    # Returns the line and the tip as individual components
    def get_components(self) -> tuple[TransLine, TransTip]:
        return (self.line, self.tip)


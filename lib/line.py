#  _______               __      ___     
# |__   __|              \ \    / (_)    
#    | |_ __ __ _ _ __  __\ \  / / _ ___ 
#    | | '__/ _` | '_ \/ __\ \/ / | / __|
#    | | | | (_| | | | \__ \\  /  | \__ \
#    |_|_|  \__,_|_| |_|___/ \/   |_|___/
#   https://git.psi.ch/hipa_apps/TransVis
#
# Implements a transoformable line which
# using catmull-ron interpolation can be
# converted into a chain of bezier curves.
#
# @Author: Adam Koprek

import numpy as np
from typing import Callable

from lib.types import PNT, PNTS, BEZ, BEZS


# Convertion Matrix used for Catmull-Ron
CONVERTER_MATRIX = (1 / 6) * np.array([[ 0, 6, 0,  0],
                                       [-1, 6, 1,  0],
                                       [ 0, 1, 6, -1],
                                       [ 0, 0, 6,  0]], dtype=np.float64)

class TransLine:
    # Creates a line with a specified amount of points 
    # from the specified cordinates. Additionally it
    # creates an extra point at both ends for later
    # interpolation
    def __init__(self, begin_x, end_x, begin_y, end_y, steps) -> None:
        self._points: PNTS = np.array([])
        self._trans_points: PNTS = np.array([])
        
        points = []
        dx = (end_x - begin_x) / steps
        dy = (end_y - begin_y) / steps

        for i in range(-1, steps + 2):
            points.append(np.array([begin_x + i * dx, begin_y + i * dy]))

        self._points = np.array(points)

    # This function takes a set of four points (P_{k-1}, P_k, P_{k+1}, P_{k+2}) and
    # constructs a cubic Bezier segment controlled by these points.
    @staticmethod
    def _points_to_bezier(pk_1: PNT, pk: PNT, pk1: PNT, pk2: PNT) -> BEZ:
        pk_1_x, pk_1_y = pk_1
        pk_x, pk_y = pk
        pk1_x, pk1_y = pk1
        pk2_x, pk2_y = pk2

        bez_x = CONVERTER_MATRIX @ np.array([[pk_1_x], [pk_x], [pk1_x], [pk2_x]])
        bez_y = CONVERTER_MATRIX @ np.array([[pk_1_y], [pk_y], [pk1_y], [pk2_y]])

        return np.column_stack((bez_x.ravel(), bez_y.ravel()))

    # This function takes a sequence of 2D points and returns a sequence of cubic
    # Bezier segments constructed from overlapping groups of 4 points.
    def _line_to_bezier(self, line: PNTS) -> BEZS:
        bezier = []
        for i in range(1, len(line) - 2):
            bezier.append(
                self._points_to_bezier(
                    line[i - 1],
                    line[i],
                    line[i + 1],
                    line[i + 2],
                )
            )

        return np.stack(bezier, axis=0)

    def get_bezier(self) -> BEZS:
        return self._line_to_bezier(self._points)

    def get_transform_bez(self) -> BEZS:
        return self._line_to_bezier(self._trans_points)

    # Applies a coordinate-wise transformation to a set of 2D points
    def transform(self, xt: Callable[[float, float], float], yt: Callable[[float, float], float]) -> None:
        transfomed = []
        for point in self._points:
            x, y = point
            transfomed.append(np.array([xt(x, y), yt(x, y)], dtype=np.float64))

        self._trans_points = np.array(transfomed)

    def trans_max(self) -> float:
        m = 0

        for point in self._trans_points:
            m = max(abs(point[0]), m)
            m = max(abs(point[1]), m)

        return m

    def scale_transformed(self, s: float) -> None:
        self._trans_points *= s


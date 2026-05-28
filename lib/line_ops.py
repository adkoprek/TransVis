#  _______               __      ___     
# |__   __|              \ \    / (_)    
#    | |_ __ __ _ _ __  __\ \  / / _ ___ 
#    | | '__/ _` | '_ \/ __\ \/ / | / __|
#    | | | | (_| | | | \__ \\  /  | \__ \
#    |_|_|  \__,_|_| |_|___/ \/   |_|___/
#   https://git.psi.ch/hipa_apps/TransVis
#
# Implements line operations which transform
# lines and interpolates them using catmull-ron
# algorithm. Allows export of lines into svg
# readable paths.
#
# @Author: Adam Koprek

import numpy as np
from typing import Callable
from lib.types import PNT, PNTS, BEZ, BEZS


CONVERTER_MATRIX = (1 / 6) * np.array([[ 0, 6, 0,  0],
                                       [-1, 6, 1,  0],
                                       [ 0, 1, 6, -1],
                                       [ 0, 0, 6,  0]], dtype=np.float64)


# This function takes a set of four points (P_{k-1}, P_k, P_{k+1}, P_{k+2}) and
# constructs a cubic Bezier segment controlled by these points.
def points_to_bezier(pk_1: PNT, pk: PNT, pk1: PNT, pk2: PNT) -> BEZ:
    pk_1_x, pk_1_y = pk_1
    pk_x, pk_y = pk
    pk1_x, pk1_y = pk1
    pk2_x, pk2_y = pk2

    bez_x = CONVERTER_MATRIX @ np.array([[pk_1_x], [pk_x], [pk1_x], [pk2_x]])
    bez_y = CONVERTER_MATRIX @ np.array([[pk_1_y], [pk_y], [pk1_y], [pk2_y]])

    return np.column_stack((bez_x.ravel(), bez_y.ravel()))


# This function takes a sequence of 2D points and returns a sequence of cubic
# Bezier segments constructed from overlapping groups of 4 points.
def line_to_bezier(line: PNTS) -> BEZS:
    bezier = []
    for i in range(1, len(line) - 2):
        bezier.append(
            points_to_bezier(
                line[i - 1],
                line[i],
                line[i + 1],
                line[i + 2],
            )
        )

    return np.stack(bezier, axis=0)


# Takes a sequence of cubic Bezier segments and returns an SVG path string
# for the d-attribute of a path element.
def construct_bezier_string(bezier: BEZS) -> str:
    r = lambda x: str(np.round(x.item(), 2))
    bezier_str = f"M {r(bezier[0][0][0])} {r(bezier[0][0][1])} "

    for i in range(len(bezier)):
        pack = bezier[i]
        bez = "C "

        for k in range(1, 4):
            bez += r(pack[k][0]) + " " + r(pack[k][1])

            if k < 3:
                bez += ", "
            else:
                bez += " "

        bezier_str += bez

    return bezier_str


# Applies a coordinate-wise transformation to a set of 2D points
def transform(points: PNTS, xt: Callable[[float, float], float], yt: Callable[[float, float], float]) -> PNTS:
    trans_points = []

    for point in points:
        x, y = point
        trans_points.append(np.array([xt(x, y), yt(x, y)], dtype=np.float64))

    return np.array(trans_points, dtype=np.float64)


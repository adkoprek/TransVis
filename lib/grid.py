#  _______               __      ___     
# |__   __|              \ \    / (_)    
#    | |_ __ __ _ _ __  __\ \  / / _ ___ 
#    | | '__/ _` | '_ \/ __\ \/ / | / __|
#    | | | | (_| | | | \__ \\  /  | \__ \
#    |_|_|  \__,_|_| |_|___/ \/   |_|___/
#   https://git.psi.ch/hipa_apps/TransVis
#
# Implements a 2D grid that has the capapilites
# to store transformable grid lines as well as
# direction vectors.
#
# @Author: Adam Koprek

from typing import Callable

import lib.document as svg
from lib.line import TransLine
from lib.vector import TransVector


class Grid:
    def __init__(self) -> None:
        self.line: list[TransLine] = []

        self.set_dir = False
        self.dir_i: TransVector
        self.dir_j: TransVector
    
    # Creates an initial cartesian grid from the specified
    # x and y points
    def init_grid(self, x_min, x_max, y_min, y_max, num) -> None:
        dx = int((x_max - x_min) / num)
        for i in range(x_min, x_max + dx, dx):
            self.line.append(TransLine(x_min, x_max, i, i, dx))

        dy = int((y_max - y_min) / num)
        for i in range(y_min, y_max + dy, dy):
            self.line.append(TransLine(i, i, x_min, x_max, dy))

    # Creates direction vectors in the direction of the unit
    # vectors with the specified lenghts
    def create_direction_vectors(self, l1: int, l2: int, side: int) -> None:
        self.set_dir = True
        self.dir_i = TransVector(0, l1, 0, 0, side) 
        self.dir_j = TransVector(0, 0, 0, l2, side) 

    # Transforms every point in the grid according to the provided
    # xt and yt transformation, also transforms the direction vectors
    # if such were created
    def transform(self, xt: Callable[[float, float], float], yt: Callable[[float, float], float]) -> None:
        for line in self.line:
            line.transform(xt, yt)

        if self.set_dir:
            self.dir_i.transform(xt, yt)
            self.dir_j.transform(xt, yt)

    # Normalises the grid to a specified width r for imporved rendering
    # for stretching of squishing functions
    def normalize(self, r: int) -> None:
        m = 0
        for line in self.line:
            m = max(line.trans_max(), m)

        for line in self.line:
            line.scale_transformed(r / m)

        if self.set_dir:
            self.dir_i.scale(r / m)
            self.dir_j.scale(r / m)

    # Paints the grid using the provided attributes to the
    # specified svg document
    def paint(self, doc: svg.Document, args: svg.AnimatedObjectParams = svg.AnimatedObjectParams()) -> None:
        for line in self.line:
            doc.create_animated_line(line, args)
    
    # Paints the direciton vectors using the provided attributes
    # to the provided svg document
    def paint_directions(
            self, doc: svg.Document, args1: svg.AnimatedObjectParams, args2: svg.AnimatedObjectParams) -> None:
        doc.create_animated_vector(self.dir_i, args1)
        doc.create_animated_vector(self.dir_j, args2)


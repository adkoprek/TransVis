#  _______               __      ___     
# |__   __|              \ \    / (_)    
#    | |_ __ __ _ _ __  __\ \  / / _ ___ 
#    | | '__/ _` | '_ \/ __\ \/ / | / __|
#    | | | | (_| | | | \__ \\  /  | \__ \
#    |_|_|  \__,_|_| |_|___/ \/   |_|___/
#   https://git.psi.ch/hipa_apps/TransVis
#
# Implements a 2D grid that has the capapilites
# to store vertical and horizontal grid lines as
# well as the functionality for direction vectors.
#
# @Author: Adam Koprek

from typing import Callable
import numpy as np
import lib.line_ops as lop
import lib.svg as svg
import lib.vec_ops as vop


class Grid:
    def __init__(self) -> None:
        self.hor = []
        self.ver = []
        self.trans_hor = []
        self.trans_ver = []
        self.dir_i = None
        self.dir_j = None
        self.trans_dir_i = np.array([])
        self.trans_dir_j = np.array([])
    
    # Creates a line with a specified amount of points 
    # from the specified cordinates. Additionally it
    # creates an extra point at both ends for later
    # interpolation
    @staticmethod
    def create_line(begin_x, end_x, begin_y, end_y, steps) -> lop.PNTS:
        dx = (end_x - begin_x) / steps
        dy = (end_y - begin_y) / steps

        line = []

        for i in range(-1, steps + 2):
            line.append([begin_x + i * dx, begin_y + i * dy])

        return np.array(line)

    # Creates an initial cartesian grid from the specified
    # x and y points
    def init_grid(self, x_min, x_max, y_min, y_max, num) -> None:
        dx = int((x_max - x_min) / num)
        for i in range(x_min, x_max + dx, dx):
            self.hor.append(self.create_line(x_min, x_max, i, i, dx))

        dy = int((y_max - y_min) / num)
        for i in range(y_min, y_max + dy, dy):
            self.ver.append(self.create_line(i, i, x_min, x_max, dy))

    # Creates direction vectors in the direction of the unit
    # vectors with the specified lenghts
    def create_direction_vectors(self, l1: int, l2: int) -> None:
        self.dir_i = self.create_line(0, l1, 0, 0, 1) 
        self.dir_j = self.create_line(0, 0, 0, l2, 1) 

    # Transforms every point in the grid according to the provided
    # xt and yt transformation, also transforms the direction vectors
    # if such were created
    def transform(self, xt: Callable[[float, float], float], yt: Callable[[float, float], float]) -> None:
        for line in self.hor:
            self.trans_hor.append(lop.transform(line, xt, yt))

        for line in self.ver:
            self.trans_ver.append(lop.transform(line, xt, yt))

        if (self.dir_i is not None) and (self.dir_j is not None):
            self.trans_dir_i = lop.transform(self.dir_i, xt, yt)
            self.trans_dir_j = lop.transform(self.dir_j, xt, yt)

    # Normalises the grid to a specified width r for imporved rendering
    # for stretching of squishing functions
    def normalize(self, r: int) -> None:
        m = 0
        for lines in (self.trans_hor, self.trans_ver):
            for line in lines:
                for e in line:
                    m = max(e[0], m)
                    m = max(e[1], m)

        for lines in (self.trans_hor, self.trans_ver):
            for line in lines:
                line /= m
                line *= r

        if (self.dir_i is not None) and (self.dir_j is not None):
            for direction in (self.trans_dir_i, self.trans_dir_j):
                direction /= m
                direction *= r

    # Paints the grid using the provided attributes to the
    # specified svg document
    def paint(self, doc: svg.Document, **kwargs) -> None:
        for lines in (zip(self.hor, self.trans_hor), zip(self.ver, self.trans_ver)):
            for line, trans in lines:
                start = lop.construct_bezier_string(lop.line_to_bezier(line))
                end = lop.construct_bezier_string(lop.line_to_bezier(trans))
                doc.create_animated_path(start, end, **kwargs)
    
    # Paints the direciton vectors using the provided attributes
    # to the provided svg document
    def paint_directions(
        self, doc: svg.Document, c1: str = "#6A9C52", c2: str = "#CE5044", l: int = 10, **kwargs):
        if (self.dir_i is not None) and (self.dir_j is not None):
            for directions in ((self.dir_i, self.trans_dir_i, c1), (self.dir_j, self.trans_dir_j, c2)):
                direction, trans_direction, color = directions
                
                direction_bez       = lop.line_to_bezier(direction)
                trans_direction_bez = lop.line_to_bezier(trans_direction)

                direction_bez_str       = lop.construct_bezier_string(direction_bez)
                trans_direction_bez_str = lop.construct_bezier_string(trans_direction_bez)

                tip_bez         = vop.tip_vertecies_from_beizer(direction_bez, l)
                trans_tip_bez   = vop.tip_vertecies_from_beizer(trans_direction_bez, l)

                tip_bez_str         = vop.vertecies_to_string(tip_bez)
                trans_tip_bez_str   = vop.vertecies_to_string(trans_tip_bez)

                doc.create_animated_vector(
                        direction_bez_str, 
                        trans_direction_bez_str, 
                        tip_bez_str, 
                        trans_tip_bez_str,
                        color=color,
                        **kwargs
                    )


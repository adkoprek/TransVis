from typing import Callable
import numpy as np
import lib.line_ops as lop
import lib.svg as svg


class Grid:
    def __init__(self) -> None:
        self.hor = []
        self.ver = []
        self.trans_hor = []
        self.trans_ver = []
        self.dir_i = None
        self.dir_j = None
        self.trans_dir_i = None
        self.trans_dir_j = None
    
    @staticmethod
    def create_line(begin_x, end_x, begin_y, end_y, steps) -> lop.PNTS:
        dx = (end_x - begin_x) / steps
        dy = (end_y - begin_y) / steps

        line = []

        for i in range(-1, steps + 2):
            line.append([begin_x + i * dx, begin_y + i * dy])

        return np.array(line)

    def init_grid(self, x_min, x_max, y_min, y_max, num) -> None:
        dx = int((x_max - x_min) / num)
        for i in range(x_min, x_max + dx, dx):
            self.hor.append(self.create_line(x_min, x_max, i, i, dx))

        dy = int((y_max - y_min) / num)
        for i in range(y_min, y_max + dy, dy):
            self.ver.append(self.create_line(i, i, x_min, x_max, dy))

    def create_direction_vectors(self, l1: int, l2: int) -> None:
        self.dir_i = self.create_line(0, l1, 0, 0, 1) 
        print(self.dir_i)
        self.dir_j = self.create_line(0, 0, 0, l2, 1) 

    def transform(self, xt: Callable[[float, float], float], yt: Callable[[float, float], float]) -> None:
        for line in self.hor:
            self.trans_hor.append(lop.transform(line, xt, yt))

        for line in self.ver:
            self.trans_ver.append(lop.transform(line, xt, yt))

        if (self.dir_i is not None) and (self.dir_j is not None):
            self.trans_dir_i = lop.transform(self.dir_i, xt, yt)
            self.trans_dir_j = lop.transform(self.dir_j, xt, yt)

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

    def paint(self, doc: svg.Document, **kwargs) -> None:
        for lines in (zip(self.hor, self.trans_hor), zip(self.ver, self.trans_ver)):
            for line, trans in lines:
                start = lop.construct_bezier_string(lop.line_to_bezier(line))
                end = lop.construct_bezier_string(lop.line_to_bezier(trans))
                doc.create_animated_path(start, end, **kwargs)

        if (self.dir_i is not None) and (self.dir_j is not None):
            for directions in ((self.dir_i, self.trans_dir_i), (self.dir_j, self.trans_dir_j)):
                direction, trans_direction = directions
                start = lop.construct_bezier_string(lop.line_to_bezier(direction))
                end = lop.construct_bezier_string(lop.line_to_bezier(trans_direction))
                doc.create_animated_path(start, end, **kwargs, color="red")


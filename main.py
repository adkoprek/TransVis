from line_trans import *
import numpy as np
from svg import Document


grid: list[PNTS] = []
doc = Document()
doc.init_document(800, 800)

def create_line(begin_x, end_x, begin_y, end_y, steps) -> PNTS:
	dx = (end_x - begin_x) / steps
	dy = (end_y - begin_y) / steps

	line = []

	for i in range(-1, steps + 2):
		line.append([begin_x + i * dx, begin_y + i * dy])

	return np.array(line)

for i in range(-400, 410, 40):
	grid.append(create_line(-400, 400, i, i, 50))
	grid.append(create_line(i, i, -400, 400, 50))


d = lambda x, y: np.sqrt(x ** 2 + y ** 2)

r = 400
l = 500
s = lambda c: r * np.tanh(c / l)

def normalize(r, grid):
	m = 0
	for line in grid:
		for e in line:
			m = max(e[0], m)
			m = max(e[1], m)

	for line in grid:
		for i in range(0, len(line)):
			line[i] /= m
			line[i] *= r

trans_grid = []
f = 700
for line in grid:
	trans = transform(
		line,
lambda x, y, k=1: (lambda xn, yn: (lambda r, t: r*np.cos(t + k*r))(np.hypot(xn, yn), np.arctan2(yn, xn)))(x/400, y/400),
lambda x, y, k=1: (lambda xn, yn: (lambda r, t: r*np.sin(t + k*r))(np.hypot(xn, yn), np.arctan2(yn, xn)))(x/400, y/400)
	)
	trans_grid.append(trans)

normalize(r, trans_grid)
for line, trans in zip(grid, trans_grid):
	start = construct_bezier_string(line_to_bezier(line))
	end = construct_bezier_string(line_to_bezier(trans))
	doc.create_animated_path(start, end, dur=5)

doc.save("svg.html")


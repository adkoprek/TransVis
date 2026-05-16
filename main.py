import numpy as np
from lib.grid_opps import Grid
from lib.svg import Document


R = 400

doc = Document()
doc.init_document(2 * R, 2 * R)
doc.set_background("black")

grid: Grid = Grid()
grid.init_grid(-R, R, -R, R, 20)
grid.transform(
    lambda x, y: 25 * np.sin(y / 80),
    lambda x, y: 25 * np.cos(x / 80)
)
grid.normalize(int(0.98 * R))
grid.paint(doc)
doc.save("svg.html")


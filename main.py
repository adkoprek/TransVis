import numpy as np

from lib.grid import Grid
from lib.document import AnimatedObjectParams, Document


R = 400

doc = Document()
doc.init_document(2 * R, 2 * R)
doc.set_background("black")
doc.add_functions(
        r"$f_x(x,y)=x \cdot \cos\left(\frac{\sqrt{x^2 + y^2}}{100} \right) - y \cdot \sin\left(\frac{\sqrt{x^2+y^2}}{100}\right)$", 
        r"$f_y(x,y)=x \cdot \cos\left(\frac{\sqrt{x^2 + y^2}}{100} \right) + y \cdot \sin\left(\frac{\sqrt{x^2+y^2}}{100}\right)$", 
        10, size=20)

d = lambda x, y: np.sqrt(x ** 2 + y ** 2)
s = 100

d = lambda x, y: np.sqrt(x ** 2 + y ** 2)
s = 100

grid: Grid = Grid()
grid.init_grid(-R, R, -R, R, 20)
grid.create_direction_vectors(40, 40, 15)
grid.transform(
    lambda x, y: x * np.cos(d(x, y) / s) - y * np.sin(d(x,y) / s),
    lambda x, y: x * np.cos(d(x, y) / s) + y * np.sin(d(x,y) / s),
)
grid.normalize(int(0.95 * R))
grid.paint(doc)
grid.paint_directions(doc, AnimatedObjectParams(color="#CF5044",width=3), AnimatedObjectParams(color="#699C52", width=3))
doc.save("example.svg")


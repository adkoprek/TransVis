import numpy as np

from lib.grid import Grid
from lib.document import AnimatedObjectParams, Document


############################### Example ########################################################
x_label = r"$f_x(x,y)=x \cdot \cos\left(\frac{\sqrt{x^2 + y^2}}{100} \right) - y \cdot \sin\left(\frac{\sqrt{x^2+y^2}}{100}\right)$"
y_label = r"$f_y(x,y)=x \cdot \cos\left(\frac{\sqrt{x^2 + y^2}}{100} \right) + y \cdot \sin\left(\frac{\sqrt{x^2+y^2}}{100}\right)$"

strech = 100

d = lambda x, y: np.sqrt(x ** 2 + y ** 2)
x_func = lambda x, y: x * np.cos(d(x, y) / strech) - y * np.sin(d(x,y) / strech)
y_func = lambda x, y: x * np.cos(d(x, y) / strech) + y * np.sin(d(x,y) / strech)
################################################################################################


radius = 400
padding_relative = 0.95
padded_radius = int(radius * padding_relative)

doc = Document()
doc.init_document(2 * radius, 2 * radius)
doc.set_background("black")
doc.add_functions(x_label, y_label, 16, size=20)


grid: Grid = Grid()
grid.init_grid(-padded_radius, padded_radius, -padded_radius, padded_radius, 20)
grid.create_direction_vectors(40, 40, 15)
grid.transform(x_func, y_func)
grid.normalize(padded_radius)
grid.paint(doc)
grid.paint_directions(doc, AnimatedObjectParams(color="#CF5044", width=3), AnimatedObjectParams(color="#699C52", width=3))
doc.save("example.svg")


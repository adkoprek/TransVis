import numpy as np
from lib.grid_ops import Grid
from lib.svg import Document


R = 400

doc = Document()
doc.init_document(2 * R, 2 * R, text_frame=int((0.7) * R))
doc.set_background("black")
doc.add_functions(
        r"$f_x(x,y)=x \cdot \cos\left(\frac{\sqrt{x^2 + y^2}}{100} \right) - y \cdot \sin\left(\frac{\sqrt{x^2+y^2}}{100}\right)$", 
        r"$f_y(x,y)=x \cdot \cos\left(\frac{\sqrt{x^2 + y^2}}{100} \right) + y \cdot \sin\left(\frac{\sqrt{x^2+y^2}}{100}\right)$", 
        10, size=20)

d = lambda x, y: np.sqrt(x ** 2 + y ** 2)
s = 100

grid: Grid = Grid()
grid.init_grid(-R, R, -R, R, 20)
grid.create_direction_vectors(60, 60)
grid.transform(
    lambda x, y: x * np.cos(d(x, y) / s) - y * np.sin(d(x,y) / s),
    lambda x, y: x * np.cos(d(x, y) / s) + y * np.sin(d(x,y) / s),
)
grid.normalize(int(1 * R))
grid.paint(doc, dur=10)
grid.paint_directions(doc, dur=10, width=4, l=10)
doc.save("svg.html")


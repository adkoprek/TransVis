from lib.line_ops import BEZS, PNTS
import numpy as np
from copy import copy


# This function takes the coefficient of a bezier curve and creates the vertecies of an arrow tip
# sits on the tangent of the last two control points with side length l and reduces the length of the line by l
def tip_vertecies_from_beizer(bezier: BEZS, l: int) -> PNTS:
    print("Bezier", bezier)
    print("l", l)
    _, _, p3, p4 = copy(bezier[0])

    h = ((3 ** 0.5) * l) / 2
    print("h", h)
    tangent = p4 - p3
    print("Tangent", tangent)
    tangent_length = (tangent[0] ** 2 + tangent[1] ** 2) ** 0.5
    print("Tangent length", tangent_length)
    tangent_proportion = h / tangent_length
    print("Tangent proportion", tangent_proportion)

    v1 = p4

    ortho = np.array([tangent[1], -tangent[0]])
    print("Ortho", ortho)
    ortho_length = (ortho[0] ** 2 + ortho[1] ** 2) ** 0.5
    print("Ortho length", ortho_length)
    ortho_prop = (l / 2) / ortho_length
    print("Ortho proportion", ortho_prop)

    v2 = p4 + ortho_prop * ortho - tangent_proportion * tangent
    v3 = p4 - ortho_prop * ortho - tangent_proportion * tangent

    bezier[0][3] -= tangent_proportion * tangent

    return np.array([v1, v2, v3])

def vertecies_to_string(vertecies: PNTS) -> str:
    out = ""
    r = lambda v: str(np.round(v, 2))

    for i, vertex in enumerate(vertecies):
        x, y = vertex
        out += f"{r(x)},{r(y)}"

        out += " " if i < len(vertecies) else ""

    return out


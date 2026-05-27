from lib.line_ops import BEZS, PNTS
import numpy as np
from copy import copy


# This function takes the coefficient of a bezier curve and creates the vertecies of an arrow tip
# sits on the tangent of the last two control points with side length l and reduces the length of the line by l
def tip_vertecies_from_beizer(bezier: BEZS, l: int) -> PNTS:
    p1, _, p3, p4 = copy(bezier[0])

    h = ((3 ** 0.5) * l) / 2
    tangent = p4 - p3
    tangent_length = (tangent[0] ** 2 + tangent[1] ** 2) ** 0.5
    tangent_proportion = h / tangent_length

    v1 = p4

    ortho = np.array([tangent[1], -tangent[0]])
    ortho_length = (ortho[0] ** 2 + ortho[1] ** 2) ** 0.5
    ortho_prop = (l / 2) / ortho_length

    v2 = p4 + ortho_prop * ortho - tangent_proportion * tangent
    v3 = p4 - ortho_prop * ortho - tangent_proportion * tangent

    bez_len = np.sqrt((p4[0] - p1[0]) ** 2 + (p4[1] - p1[1]) ** 2)
    bezier *= (bez_len - h * 0.9) / bez_len

    return np.array([v1, v2, v3])

def vertecies_to_string(vertecies: PNTS) -> str:
    out = ""
    r = lambda v: str(np.round(v, 2))

    for i, vertex in enumerate(vertecies):
        x, y = vertex
        out += f"{r(x)},{r(y)}"

        out += " " if i < len(vertecies) else ""

    return out


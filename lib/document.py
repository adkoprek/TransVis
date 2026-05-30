#  _______               __      ___     
# |__   __|              \ \    / (_)    
#    | |_ __ __ _ _ __  __\ \  / / _ ___ 
#    | | '__/ _` | '_ \/ __\ \/ / | / __|
#    | | | | (_| | | | \__ \\  /  | \__ \
#    |_|_|  \__,_|_| |_|___/ \/   |_|___/
#   https://git.psi.ch/hipa_apps/TransVis
#
# Provides an interface to operate on svg
# documents. It is designed to support the
# operations for animated paths and vectors.
#
# @Author: Adam Koprek

import io
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from xml.dom import minidom, Node

from lib.types import PNTS, BEZS
from lib.line import TransLine
from lib.vector import TransTip, TransVector


@dataclass
class AnimatedObjectParams:
    color: str = "#58C4DD"
    width: int = 1
    dur: float = 10

# This class handles SVG (XML) data using minidom
class Document:
    root: minidom.Document
    svg: minidom.Element
    grid: minidom.Element
    text_offset: int

    # Creates a document
    def __init__(self) -> None:
        self.root = minidom.Document()
    
    # Initializes an empty XML document and a grid which is flipped to
    # be mathematically aligned correctly
    def init_document(self, width: int, height: int, text_frame: int = 0) -> None:
        self.svg = self.root.createElement("svg")
        self.svg.setAttribute("xmlns", "http://www.w3.org/2000/svg")
        self.svg.setAttribute("version", "1.1")
        self.svg.setAttribute("width", f"{width}px")
        self.svg.setAttribute("height", f"{height + text_frame}px")
        self.svg.setAttribute("viewBox", f"{-width / 2} {-height / 2} {width} {height + text_frame}")
        self.root.appendChild(self.svg)

        # Converts the grid into a Cartesian coordinate system
        self.grid = self.root.createElement("g")
        self.grid.setAttribute("transform", "scale(1,-1)")
        self.svg.appendChild(self.grid)

        self.text_offset = int(height / 2)

    # Creates a background for the entire canvas
    def set_background(self, color: str) -> None:
        background = self.root.createElement("rect")
        background.setAttribute("x", "-50%")
        background.setAttribute("y", "-50%")
        background.setAttribute("width", "100%")
        background.setAttribute("height", "100%")
        background.setAttribute("fill", color)
        self.svg.insertBefore(background, self.grid)


    # Creates a minidom.Element SVG from the provided LaTeX inline math equation
    # it returns a group containing the math block and the dimensions of the equation
    @staticmethod
    def latex_to_svg(latex, size: int = 24, color: str = "white") -> tuple[minidom.Element, tuple[float, float]]:
        fig = plt.figure()
        text = fig.text(0, 0, latex, color=color, fontsize=size)
        plt.axis("off")

        # Resize `````````````````````````````````````````````````````````````````````````
        fig.canvas.draw()
        bbox = text.get_window_extent()
        dpi = fig.dpi
        width = bbox.width / dpi
        height = bbox.height / dpi
        fig.set_size_inches(width, height)

        buffer = io.StringIO()
        fig.savefig(
            buffer,
            format="svg",
            bbox_inches="tight",
            pad_inches=0.1,
            transparent=True
        )

        svg_text = buffer.getvalue()
        mat_svg = minidom.parseString(svg_text)
        svg_root = mat_svg.getElementsByTagName("svg")[0]

        svg_width = float(svg_root.getAttribute("width").replace("pt", ""))
        svg_height = float(svg_root.getAttribute("height").replace("pt", ""))

        svg = minidom.Document()
        group = svg.createElement("g")

        for node in mat_svg.documentElement.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                if node.tagName in ["g", "defs"]:
                    group.appendChild(node)

        svg.appendChild(group)

        return (group, (svg_width, svg_height))

    # Adds function descriptions to the bottom of the animation using
    # the provided LaTeX code and padding.
    def add_functions(self, latex_x: str, latex_y: str, padding: int, color: str = "white", size: int = 24):
        x_label, x_dim = self.latex_to_svg(latex_x, color=color, size=size)
        x_label.setAttribute("transform", f"translate({-x_dim[0] / 2}, {self.text_offset + padding})")
        y_label, y_dim = self.latex_to_svg(latex_y, color=color, size=size)
        y_label.setAttribute("transform", f"translate({-y_dim[0] / 2}, {self.text_offset + padding + x_dim[1]})")

        self.svg.appendChild(x_label)
        self.svg.appendChild(y_label)

    # Takes a sequence of cubic Bezier segments and returns an SVG path string
    # for the d-attribute of a path element.
    @staticmethod
    def construct_bezier_string(bezier: BEZS) -> str:
        r = lambda x: str(np.round(x.item(), 2))
        bezier_str = f"M {r(bezier[0][0][0])} {r(bezier[0][0][1])} "

        for i in range(len(bezier)):
            pack = bezier[i]
            bez = "C "

            for k in range(1, 4):
                bez += r(pack[k][0]) + " " + r(pack[k][1])

                if k < 3:
                    bez += ", "
                else:
                    bez += " "

            bezier_str += bez

        return bezier_str

    # Converts the vertices of a vector tip to an SVG-readable string
    @staticmethod
    def vertices_to_string(vertices: PNTS) -> str:
        out = ""
        r = lambda v: str(np.round(v, 2))

        for i, vertex in enumerate(vertices):
            x, y = vertex
            out += f"{r(x)},{r(y)}"

            out += " " if i < len(vertices) - 1 else ""

        return out

    # Constructs and returns an animated path from the provided SVG d-path (start to end)
    def _construct_animated_path(self, line: TransLine, args: AnimatedObjectParams) -> minidom.Element:
        path = self.root.createElement("path")
        path.setAttribute("stroke", args.color)
        path.setAttribute("stroke-width", str(args.width))
        path.setAttribute("fill", "none")

        line_bez = line.get_bezier()
        trans_line_bez = line.get_transform_bez()

        animate = self.root.createElement("animate")
        animate.setAttribute("from", self.construct_bezier_string(line_bez))
        animate.setAttribute("to", self.construct_bezier_string(trans_line_bez))
        animate.setAttribute("dur", f"{args.dur}s")
        animate.setAttribute("attributeName", "d")
        animate.setAttribute("fill", "freeze")

        path.appendChild(animate)

        return path

    # Creates an animated vector tip from the triangle vertices
    def _construct_animated_tip(self, tip: TransTip, args: AnimatedObjectParams) -> minidom.Element:
        polygon = self.root.createElement("polygon")
        polygon.setAttribute("stroke", "none")
        polygon.setAttribute("fill", args.color)

        animate = self.root.createElement("animate")

        tip_vertices = tip.get_tip()
        trans_tip_vertices = tip.get_trans_tip()

        animate.setAttribute("from", self.vertices_to_string(tip_vertices))
        animate.setAttribute("to", self.vertices_to_string(trans_tip_vertices))
        animate.setAttribute("dur", f"{args.dur}s")
        animate.setAttribute("attributeName", "points")
        animate.setAttribute("fill", "freeze")

        polygon.appendChild(animate)

        return polygon

    # Creates an animated vector from the path and the vector tip's vertices
    def create_animated_vector(self, vector: TransVector, args: AnimatedObjectParams) -> None:
        vec = self.root.createElement("g")
        v_line, v_tip = vector.get_components()

        lin = self._construct_animated_path(v_line, args)
        tip = self._construct_animated_tip(v_tip, args)

        vec.appendChild(lin)
        vec.appendChild(tip)
        self.grid.appendChild(vec)

    # Creates an animated path from the provided SVG d-path (start to end)
    def create_animated_line(self, line: TransLine, args: AnimatedObjectParams) -> None:
        path = self._construct_animated_path(line, args)
        self.grid.appendChild(path)

    # Returns the SVG content as a string
    def get_str(self) -> str:
        return self.root.documentElement.toprettyxml(indent="\t")

    # Saves the SVG to a file
    def save(self, path: str) -> None:
        with open(path, "w+") as file:
            file.write(self.get_str())
        

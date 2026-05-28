import io
from xml.dom import minidom, Node
import matplotlib.pyplot as plt


# This class handles svg a.k.a xml data using minidom
class Document:
    root: minidom.Document
    svg: minidom.Element
    grid: minidom.Element
    text_offset: int

    # Creates a document
    def __init__(self) -> None:
        self.root = minidom.Document()
    
    # Initializes an empty xml document and grid which is flipped to
    # be maathematically aligned correctly 
    def init_document(self, width: int, height: int, text_frame: int = 0) -> None:
        self.svg = self.root.createElement("svg")
        self.svg.setAttribute("xmlns", "http://www.w3.org/2000/svg")
        self.svg.setAttribute("version", "1.1")
        self.svg.setAttribute("width", f"{width}px")
        self.svg.setAttribute("height", f"{height + text_frame}px")
        self.svg.setAttribute("viewBox", f"{-width / 2} {-height / 2} {width} {height + text_frame}")
        self.root.appendChild(self.svg)

        self.grid = self.root.createElement("g")
        self.grid.setAttribute("transform", "scale(1,-1)")
        self.svg.appendChild(self.grid)

        self.text_offset = int(height / 2)


    @staticmethod
    def latex_to_svg(latex, size: int = 24, color: str = "white") -> minidom.Element:
        fig = plt.figure()
        text = fig.text(0, 0, latex, color=color, fontsize=size)

        # Resize `````````````````````````````````````````````````````````````````````````
        fig.canvas.draw()
        bbox = text.get_window_extent()
        dpi = fig.dpi
        width = bbox.width / dpi
        height = bbox.height / dpi
        fig.set_size_inches(width, height)

        plt.axis("off")

        buffer = io.StringIO()

        fig.savefig(
            buffer,
            format="svg",
            bbox_inches="tight",
            pad_inches=0.1,
            transparent=True
        )

        svg_text = buffer.getvalue()
        svg_root = minidom.parseString(svg_text)

        svg = minidom.Document()
        group = svg.createElement("g")
        
        for node in svg_root.documentElement.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                if node.tagName in ["g", "defs"]:
                    group.appendChild(node)

        svg.appendChild(group)

        return group


    def add_functions(self, latex_x: str, latex_y: str, padding: int, color: str = "white", size: int = 24):
        x_label = self.latex_to_svg(latex_x, color=color, size=size)
        x_label.setAttribute("transform", f"translate(-215, {self.text_offset + padding})")
        y_label = self.latex_to_svg(latex_y, color=color, size=size)
        y_label.setAttribute("transform", f"translate(-215, {self.text_offset + padding + 57})")

        self.svg.appendChild(x_label)
        self.svg.appendChild(y_label)

    # Creates a background
    def set_background(self, color: str) -> None:
        background = self.root.createElement("rect")
        background.setAttribute("x", "-50%")
        background.setAttribute("y", "-50%")
        background.setAttribute("width", "100%")
        background.setAttribute("height", "100%")
        background.setAttribute("fill", color)
        self.svg.insertBefore(background, self.grid)

    def construct_animated_tip(
        self, triangle_init: str, triangle_end: str, color: str, dur: float = 2) -> minidom.Element:
        path = self.root.createElement("polygon")
        path.setAttribute("stroke", "none")
        path.setAttribute("fill", color)

        animate = self.root.createElement("animate")
        animate.setAttribute("from", triangle_init)
        animate.setAttribute("to", triangle_end)
        animate.setAttribute("dur", f"{dur}s")
        animate.setAttribute("attributeName", "points")
        animate.setAttribute("fill", "freeze")

        path.appendChild(animate)

        return path

    def create_animated_vector(
        self, line_init: str, line_end: str, triangle_init: str, triangle_end: str,
        color: str, width: int = 1, dur: float = 2) -> None:
        vec = self.root.createElement("g")
        lin = self.construct_animated_path(line_init, line_end, color=color, width=width, dur=dur)
        tip = self.construct_animated_tip(triangle_init, triangle_end, color, dur=dur)
        vec.appendChild(lin)
        vec.appendChild(tip)
        self.grid.appendChild(vec)

    def construct_animated_path(
        self, init: str, end: str, color: str = "#58C4DD", width: int = 1, dur: float = 2) -> minidom.Element:
        path = self.root.createElement("path")
        path.setAttribute("stroke", color)
        path.setAttribute("stroke-width", str(width))
        path.setAttribute("fill", "none")

        animate = self.root.createElement("animate")
        animate.setAttribute("from", init)
        animate.setAttribute("to", end)
        animate.setAttribute("dur", f"{dur}s")
        animate.setAttribute("attributeName", "d")
        animate.setAttribute("fill", "freeze")

        path.appendChild(animate)

        return path

    # Creates an animation between two paths
    def create_animated_path(
        self, init: str, end: str, color: str = "#58C4DD", width: int = 1, dur: float = 2) -> None:
        path = self.construct_animated_path(init, end, color=color, width=width, dur=dur)
        self.grid.appendChild(path)

    # Returns the svg content as a string
    def get_str(self) -> str:
        return self.root.documentElement.toprettyxml(indent="\t")

    # Saves the svg to a file
    def save(self, path: str) -> None:
        with open(path, "w+") as file:
            file.write(self.get_str())

        

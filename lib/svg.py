from xml.dom import minidom


# This class handles svg a.k.a xml data using minidom
class Document:
    root: minidom.Document
    svg: minidom.Element
    grid: minidom.Element

    # Creates a document
    def __init__(self) -> None:
        self.root = minidom.Document()
    
    # Initializes an empty xml document and grid which is flipped to
    # be maathematically aligned correctly 
    def init_document(self, width: int, height: int) -> None:
        self.svg = self.root.createElement("svg")
        self.svg.setAttribute("xmlns", "http://www.w3.org/2000/svg")
        self.svg.setAttribute("version", "1.1")
        self.svg.setAttribute("width", f"{width}px")
        self.svg.setAttribute("height", f"{height}px")
        self.svg.setAttribute("viewBox", f"{-width / 2} {-height / 2} {width} {height}")
        self.root.appendChild(self.svg)

        self.grid = self.root.createElement("g")
        self.grid.setAttribute("transform", "scale(1,-1)")
        self.svg.appendChild(self.grid)

    # Creates a background
    def set_background(self, color: str) -> None:
        background = self.root.createElement("rect")
        background.setAttribute("x", "-50%")
        background.setAttribute("y", "-50%")
        background.setAttribute("width", "100%")
        background.setAttribute("height", "100%")
        background.setAttribute("fill", color)
        self.svg.insertBefore(background, self.grid)
    
    # Creates an animation between two paths
    def create_animated_path(
        self, init: str, end: str, color: str = "#58C4DD", width: int = 1, dur: float = 2) -> None:
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
        self.grid.appendChild(path)

    # Returns the svg content as a string
    def get_str(self) -> str:
        return self.root.documentElement.toprettyxml(indent="\t")

    # Saves the svg to a file
    def save(self, path: str) -> None:
        with open(path, "w+") as file:
            file.write(self.get_str())

        

from xml.dom import minidom


class Document:
    root: minidom.Document
    svg: minidom.Element

    def __init__(self) -> None:
        self.root = minidom.Document()
    
    def init_document(self, width: int, height: int) -> None:
        self.svg = self.root.createElement("svg")
        self.svg.setAttribute("xmlns", "http://www.w3.org/2000/svg")
        self.svg.setAttribute("version", "1.1")
        self.svg.setAttribute("width", f"{width}px")
        self.svg.setAttribute("height", f"{height}px")
        self.svg.setAttribute("viewBox", f"{-width / 2} {-height / 2} {width} {height}")
        self.root.appendChild(self.svg)

    def set_background(self, color: str) -> None:
        background = self.root.createElement("rect")
        background.setAttribute("x", "-50%")
        background.setAttribute("y", "-50%")
        background.setAttribute("width", "100%")
        background.setAttribute("height", "100%")
        background.setAttribute("fill", color)
        self.svg.appendChild(background)

    def create_animated_path(
        self, init: str, end: str, color: str = "black", width: int = 1, dur: float = 2) -> None:
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
        self.svg.appendChild(path)

    def get_str(self) -> str:
        return self.root.documentElement.toprettyxml(indent="\t")

    def save(self, path: str) -> None:
        with open(path, "w+") as file:
            file.write(self.get_str())

        

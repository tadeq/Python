from PIL import Image, ImageDraw
from figures import Point
from figures import Polygon
from figures import Rectangle
from figures import Square
from figures import Circle


class Display:
    def __init__(self, figures, screen, palette=None):
        self.figures = figures
        self.screen = screen
        if palette is None:
            self.palette = dict()
        else:
            self.palette = palette
        self.img = None

    def set_bg(self):
        bg_color = self.screen['bg_color']
        width = self.screen['width']
        height = self.screen['height']
        if bg_color[0] in "(#":
            self.img = Image.new('RGB', (width, height), bg_color)
        else:
            self.img = Image.new('RGB', (width, height), self.palette[bg_color])

    def set_color(self, color):
        if color[0] == "#":
            return color
        elif color[0] == "(":
            col = color[1:-1].split(",")
            col = [int(rgb) for rgb in col]
            return tuple(col)
        else:
            return self.palette[color]

    def draw_figures(self):
        draw = ImageDraw.Draw(self.img)
        for figure in self.figures:
            t = type(figure)
            if figure.color is not None:
                col = figure.color
            else:
                col = self.screen['fg_color']
            col = self.set_color(col)
            if t == Point:
                draw.point([figure.x, figure.y], fill=col)
            elif t == Polygon:
                draw.polygon([(v.x, v.y) for v in figure.vertexes], fill=col)
            elif t == Rectangle:
                rect = [(figure.center.x - figure.width / 2, figure.center.y - figure.height / 2),
                        (figure.center.x + figure.width / 2, figure.center.y + figure.height / 2)]
                draw.rectangle(rect, fill=col)
            elif t == Square:
                square = [(figure.center.x - figure.size / 2, figure.center.y - figure.size / 2),
                          (figure.center.x + figure.size / 2, figure.center.y + figure.size / 2)]
                draw.rectangle(square, fill=col)
            elif t == Circle:
                circle = [(figure.center.x - figure.radius, figure.center.y - figure.radius),
                          (figure.center.x + figure.radius, figure.center.y + figure.radius)]
                draw.ellipse(circle, fill=col)

    def display(self):
        self.set_bg()
        self.draw_figures()
        self.show()

    def show(self):
        self.img.show()

    def save(self, filename):
        if not filename.endswith(tuple([".png", ".PNG"])):
            filename += ".png"
        self.img.save(filename)

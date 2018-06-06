from figures import FIGURE_TYPES
from string import hexdigits


class Validator:
    def __init__(self, figures, screen, palette=None):
        self.figures = figures
        self.screen = screen
        if palette is None:
            self.palette = dict()
        else:
            self.palette = palette

    def validate_screen(self):
        if "width" not in self.screen:
            raise ValueError("Screen width missing in json file")
        if "height" not in self.screen:
            raise ValueError("Screen height missing in json file")
        if "bg_color" in self.screen:
            self.validate_color(self.screen['bg_color'])
        if "fg_color" in self.screen:
            self.validate_color(self.screen['fg_color'])

    def validate_color(self, color):
        if color is not None:
            if color == "":
                raise ValueError("Color is empty")
            elif color[0] == "(":
                if color[-1] != ")":
                    raise ValueError("Wrong color value")
                rgb = color[1:-1]
                rgb = rgb.split(",")
                if len(rgb) != 3:
                    raise ValueError("Wrong color value")
                if not all(0 <= int(col) <= 255 for col in rgb):  # cast to int can also cause ValueError
                    raise ValueError("Wrong RGB color value")
            elif color[0] == "#":
                if len(color) != 7:
                    raise ValueError("Wrong html color value")
                if not all(char in hexdigits for char in color[1:]):
                    raise ValueError("Wrong html color value")
            elif not self.palette:
                raise ValueError("Color not html or RGB and no palette given")
            elif color not in self.palette:
                raise ValueError("No such color in palette")

    def validate_palette(self):
        for col in self.palette.values():
            self.validate_color(col)

    def validate_figures(self):
        for figure in self.figures:
            if "type" not in figure:
                raise ValueError("Missing figure type")
            t = figure['type']
            if t not in FIGURE_TYPES:
                raise ValueError("Wrong figure type")
            if t != "polygon":
                if "x" not in figure or "y" not in figure:
                    raise ValueError("Missing point coordinate")
                int(figure['x'])
                int(figure['y'])
                if t == "rectangle":
                    if "width" not in figure or "height" not in figure:
                        raise ValueError("Missing rectangle size")
                    int(figure['width'])
                    int(figure['height'])
                if t == "square":
                    if "size" not in figure:
                        raise ValueError("Missing square size")
                    int(figure['size'])
                if t == "circle":
                    if "radius" not in figure:
                        raise ValueError("Missing circle radius")
                    int(figure['radius'])
            else:
                if "points" not in figure:
                    raise ValueError("Missing rectangle points list")
                if len(figure['points']) < 3:
                    raise ValueError("Too few points to create rectangle")
                for point in figure['points']:
                    for coord in point:
                        int(coord)
            if "color" in figure:
                self.validate_color(figure['color'])
            elif "fg_color" not in self.screen:
                raise ValueError("Neither figure nor foreground color given")

    def validate_all(self):
        self.validate_screen()
        self.validate_palette()
        self.validate_figures()

    @staticmethod
    def validate_data(data):
        if "Screen" not in data:
            raise ValueError("Missing Screen data")
        if "Figures" not in data:
            raise ValueError("Missing Figures data")

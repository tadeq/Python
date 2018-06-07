FIGURE_TYPES = ["point", "polygon", "rectangle", "square", "circle"]


class Point:
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color


class Figure:
    def __init__(self, x, y, color=None):
        self.center = Point(x, y)
        self.color = color


class Polygon:
    def __init__(self, vertexes, color=None):
        self.vertexes = [Point(vertex[0], vertex[1]) for vertex in vertexes]
        self.color = color


class Rectangle(Figure):
    def __init__(self, x, y, width, height, color=None):
        super().__init__(x, y, color)
        self.width = width
        self.height = height


class Square(Rectangle):
    def __init__(self, x, y, size, color=None):
        super().__init__(x, y, size, size, color)


class Circle(Figure):
    def __init__(self, x, y, radius, color=None):
        super().__init__(x, y, color)
        self.radius = radius

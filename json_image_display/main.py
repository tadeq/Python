import json
import argparse
from figures import Point, Polygon, Rectangle, Square, Circle
from display import Display
from validator import Validator


def read_json(filename):
    with open(filename) as file:
        json_data = json.load(file)
    return json_data


def load_figures(json_figures):
    figs = []
    for fig in json_figures:
        t = fig['type']
        if t == "point":
            figs.append(Point(int(fig['x']), int(fig['y'])))
        elif t == "polygon":
            figs.append(Polygon(fig['points']))
        elif t == "rectangle":
            figs.append(Rectangle(int(fig['x']), int(fig['y']), int(fig['width']), int(fig['height'])))
        elif t == "square":
            figs.append(Square(int(fig['x']), int(fig['y']), int(fig['size'])))
        elif t == "circle":
            figs.append(Circle(int(fig['x']), int(fig['y']), int(fig['radius'])))
        if "color" in fig:
            figs[-1].color = fig['color']
    return figs


def load_data(json_data):
    figures = json_data['Figures']
    screen = json_data['Screen']
    if "Palette" in json_data:
        palette = json_data['Palette']
    else:
        palette = None
    return figures, screen, palette


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('json_filename', type=str, help='Input json file to read')
    parser.add_argument('-o', '--output', type=str, metavar='', help='Output png file to save the image')
    args = parser.parse_args()
    json_filename = args.json_filename
    if args.output is not None:
        out_filename = args.output
    else:
        out_filename = ""
    try:
        json_data = read_json(json_filename)
    except FileNotFoundError as e:
        print(e)
        return
    except json.decoder.JSONDecodeError as e:
        print(e)
        return
    try:
        Validator.validate_data(json_data)
        figures, screen, palette = load_data(json_data)
        validator = Validator(figures, screen, palette)
        validator.validate_all()
    except ValueError as e:
        print(e)
        return
    figures = load_figures(figures)
    display = Display(figures, screen, palette)
    display.display()
    if out_filename:
        display.save(out_filename)


if __name__ == "__main__":
    main()

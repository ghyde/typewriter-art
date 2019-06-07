#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw


BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)
SIDE_MARGIN = 30
TOP_MARGIN = 30
CHAR_HEIGHT = 8
CHAR_WIDTH = 4
IMAGE_DIMENSIONS = (CHAR_WIDTH * 200, CHAR_HEIGHT * 200)
DEBUG = True


def draw_line(
    draw,
    line_number,
    text,
    font=None,
    text_color=(0, 0, 0),
    margin=(SIDE_MARGIN, TOP_MARGIN),
    char_height=CHAR_HEIGHT,
):
    draw.text(
        (margin[0], margin[1] + char_height * line_number),
        text,
        fill=text_color,
        font=font,
    )


def draw_picture(file_path, font=None):
    # Get data from picture file
    with open(file_path) as f:
        data = f.read()

    # Create image object
    img = Image.new("RGBA", IMAGE_DIMENSIONS, BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    for l in data.split("\n"):
        # Ignore empty lines or comments
        if len(l) == 0 or l.startswith("#"):
            continue

        columns = l.split(" ")

        # Grab line number
        line_number = columns[0].replace(")", "")
        if DEBUG:
            print(line_number, flush=True)
        if len(line_number) > 1 and line_number[-1].isalpha():
            line_number = int(line_number[:-1])
        else:
            line_number = int(line_number)

        line_number = int(line_number)

        # Generate text for this line
        output = ""
        for c in columns[1:]:
            c = c.replace("sp", " ")
            try:
                output += c[-1] * int(c[:-1])
            except IndexError as e:
                print(c)
                raise e

        # Draw text
        draw_line(draw, line_number, output, font)

    return img


if __name__ == "__main__":
    font = ImageFont.load_path("./fonts/ctrld-fixed-16b.pil")
    img = draw_picture("./pictures/test.txt", font)
    img.save("test.png")

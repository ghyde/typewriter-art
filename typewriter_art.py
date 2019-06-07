#!/usr/bin/env python3

import os

import click
from PIL import Image, ImageFont, ImageDraw


CHAR_HEIGHT = 7
CHAR_WIDTH = 4
IMAGE_DIMENSIONS = (CHAR_WIDTH * 200, CHAR_HEIGHT * 200)


def __draw_line(
    draw,
    line_number,
    text,
    font=None,
    text_color=(0, 0, 0),
    margin=30,
    char_height=CHAR_HEIGHT,
):
    draw.text(
        (margin, margin + char_height * line_number), text, fill=text_color, font=font
    )


def __draw_picture(file_path, font=None, background_color=(255, 255, 255), **kwargs):
    # Get data from picture file
    with open(file_path) as f:
        data = f.read()

    # Create image object
    img = Image.new("RGBA", IMAGE_DIMENSIONS, background_color)
    draw = ImageDraw.Draw(img)

    for l in data.split("\n"):
        # Ignore empty lines or comments
        if len(l) == 0 or l.startswith("#"):
            continue

        columns = l.split(" ")

        # Grab line number
        line_number = columns[0].replace(")", "")
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
            except (IndexError, ValueError) as e:
                error_string = f'''Error parsing picture file "{file_path}"
    Line: {l}
    Character: "{c}"'''
                raise SystemExit(error_string)

        # Draw text
        __draw_line(draw, line_number, output, font, **kwargs)

    return img


def __generate_output_file_name(input_file_path, output_extension="png"):
    """
    Creates a file name based upon the input file's name.
    """

    # Remove the path
    base = os.path.basename(input_file_path)
    # Remove the file extension
    file_name = os.path.splitext(base)[0]

    return f"{file_name}.{output_extension}"


@click.command()
@click.argument("picture_file", required=1)
@click.option("-f", "--font", "font_file", default=None, help="Path to PIL font file.")
@click.option("-o", "--output", "output_file", help="Path to output file.")
@click.option("-H", "--char-height", default=CHAR_HEIGHT, help="Height of characters.")
def generate_picture(
    picture_file, font_file=None, output_file=None, char_height=CHAR_HEIGHT
):

    # Generate an output file name if one isn't provided
    if output_file == None:
        output_file = __generate_output_file_name(picture_file)

    # Load font file or set to None
    try:
        font = ImageFont.load_path(font_file)
    except AttributeError as e:
        font = None

    img = __draw_picture(picture_file, font, char_height=char_height)
    img.save(output_file)


if __name__ == "__main__":
    generate_picture()

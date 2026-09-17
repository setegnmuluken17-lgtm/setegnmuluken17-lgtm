from PIL import Image, ImageDraw, ImageFont
import random
import math
import os

SOURCE = "assets/source.png"
OUTPUT = "assets/ascii-animation.gif"

ASCII_CHARS = "@#8&o:*. "
WIDTH = 80
FONT_SIZE = 10
FRAMES = 24
FRAME_DURATION = 80


def convert_to_ascii(image):
    image = image.convert("L")

    aspect_ratio = image.height / image.width
    height = int(aspect_ratio * WIDTH * 0.5)

    image = image.resize((WIDTH, height))

    pixels = list(image.getdata())

    lines = []

    for y in range(height):
        line = ""

        for x in range(WIDTH):
            pixel = pixels[y * WIDTH + x]

            index = int(
                pixel / 255 * (len(ASCII_CHARS) - 1)
            )

            line += ASCII_CHARS[index]

        lines.append(line)

    return lines


def create_frame(lines, frame_number):
    width = max(len(line) for line in lines)
    height = len(lines)

    canvas_width = width * FONT_SIZE
    canvas_height = height * FONT_SIZE

    image = Image.new(
        "RGB",
        (canvas_width, canvas_height),
        (8, 12, 18)
    )

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(
            "DejaVuSansMono.ttf",
            FONT_SIZE
        )
    except:
        font = ImageFont.load_default()

    for y, line in enumerate(lines):

        wave = int(
            math.sin(
                frame_number * 0.5 + y * 0.25
            ) * 2
        )

        for x, char in enumerate(line):

            if char == " ":
                continue

            # Glitch effect
            if random.random() < 0.03:
                char = random.choice("@#$%&*+=-:.")

            brightness = random.randint(150, 255)

            draw.text(
                (
                    x * FONT_SIZE + wave,
                    y * FONT_SIZE
                ),
                char,
                fill=(brightness, brightness, brightness),
                font=font
            )

    return image


def main():

    if not os.path.exists(SOURCE):
        raise FileNotFoundError(
            f"Source image not found: {SOURCE}"
        )

    os.makedirs("assets", exist_ok=True)

    source = Image.open(SOURCE)

    lines = convert_to_ascii(source)

    frames = []

    for frame_number in range(FRAMES):
        frame = create_frame(lines, frame_number)
        frames.append(frame)

    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=0
    )

    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    main()

from PIL import Image, ImageDraw, ImageFont
import random
import os

SOURCE = "assets/source.png"
OUTPUT = "assets/ascii-animation.gif"

ASCII_CHARS = "@#8&o:*. "
WIDTH = 50
FONT_SIZE = 10

FRAMES = 40
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

            # INVERT brightness
            # Dark = space
            # Bright = ASCII character
            brightness = 255 - pixel

            index = int(
                brightness / 255 * (len(ASCII_CHARS) - 1)
            )

            line += ASCII_CHARS[index]

        lines.append(line)

    return lines


def create_frame(lines, visible_lines, glitch=False):

    width = max(len(line) for line in lines)
    height = len(lines)

    image = Image.new(
        "RGB",
        (width * FONT_SIZE, height * FONT_SIZE),
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

    # Only show lines from TOP to BOTTOM
    for y in range(visible_lines):

        line = lines[y]

        for x, char in enumerate(line):

            # Don't draw spaces
            if char == " ":
                continue

            # Small glitch effect
            if glitch and random.random() < 0.015:
                char = random.choice("@#$%&*+=-:.")

            brightness = random.randint(180, 255)

            draw.text(
                (
                    x * FONT_SIZE,
                    y * FONT_SIZE
                ),
                char,
                fill=(
                    brightness,
                    brightness,
                    brightness
                ),
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

    total_lines = len(lines)

    frames = []

    # --------------------------------
    # TOP → BOTTOM REVEAL
    # --------------------------------

    for frame_number in range(FRAMES):

        progress = (frame_number + 1) / FRAMES

        visible_lines = int(
            total_lines * progress
        )

        frame = create_frame(
            lines,
            visible_lines,
            glitch=True
        )

        frames.append(frame)

    # --------------------------------
    # HOLD COMPLETE IMAGE
    # --------------------------------

    for _ in range(10):

        frame = create_frame(
            lines,
            total_lines,
            glitch=True
        )

        frames.append(frame)

    # --------------------------------
    # SAVE GIF
    # --------------------------------

    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=0
    )

    print(
        f"Created: {OUTPUT}"
    )


if __name__ == "__main__":
    main()

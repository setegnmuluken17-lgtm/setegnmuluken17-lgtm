from PIL import Image, ImageDraw, ImageFont
import random
import os

SOURCE = "assets/source.png"
OUTPUT = "assets/ascii-animation.gif"

ASCII_CHARS = "@#8&o:*. "
WIDTH = 80
FONT_SIZE = 10

# Number of animation frames
FRAMES = 35

# Speed of each frame in milliseconds
FRAME_DURATION = 70


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


def create_frame(lines, visible_lines, frame_number):

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

    # Draw only from TOP to BOTTOM
    for y in range(min(visible_lines, height)):

        for x, char in enumerate(lines[y]):

            if char == " ":
                continue

            # Small glitch effect
            if random.random() < 0.02:
                char = random.choice("@#$%&*+=-:.")

            brightness = random.randint(170, 255)

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

    # TOP → BOTTOM animation
    for frame_number in range(FRAMES):

        progress = (frame_number + 1) / FRAMES

        visible_lines = int(
            total_lines * progress
        )

        frame = create_frame(
            lines,
            visible_lines,
            frame_number
        )

        frames.append(frame)

    # Keep the completed image for a moment
    for _ in range(8):
        frames.append(
            create_frame(
                lines,
                total_lines,
                FRAMES
            )
        )

    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=0
    )

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()

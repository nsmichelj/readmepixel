import io
import math

import cairosvg
from PIL import Image, ImageDraw, ImageFont


def create_skill_image(
    icons: list[str], icon_size: int, per_lines: int | None, spacing: int
):
    num_icons = len(icons)

    if not per_lines or per_lines > num_icons or per_lines < 1:
        per_lines = num_icons

    rows = math.ceil(num_icons / per_lines)

    # Calculate total image dimensions
    total_width = (per_lines * icon_size) + (max(0, per_lines - 1) * spacing)
    total_height = (rows * icon_size) + (max(0, rows - 1) * spacing)

    skill_image = Image.new("RGBA", (total_width, total_height), "rgba(0, 0, 0, 0)")

    for i, icon in enumerate(icons):
        png_data = cairosvg.svg2png(
            bytestring=icon, output_width=icon_size, output_height=icon_size
        )
        if not isinstance(png_data, bytes):
            continue

        icon_image = Image.open(io.BytesIO(png_data)).convert("RGBA")

        row = i // per_lines
        col = i % per_lines
        x_offset = col * (icon_size + spacing)
        y_offset = row * (icon_size + spacing)

        skill_image.paste(icon_image, (x_offset, y_offset), icon_image)

    output_buffer = io.BytesIO()
    skill_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return output_buffer


def create_badge_image(
    text: str,
    font_size: int = 14,
    padding: int = 10,
    line_spacing: int = 10,
    max_width: float | None = None,
    border_radius: int = 0,
    background: str = "#4A90E2",
    foreground: str = "white",
    border_color: str = "#00000000",
    border_width: int = 2,
):
    font_path = "./static/fonts/Roboto-Bold.ttf"

    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))

    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_width = draw.textbbox((0, 0), test_line, font=font)[2]

            if test_width <= max_width or not current_line:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    if max_width is None:
        max_width = font.getlength(text) * 1.2

    lines = wrap_text(text, font, max_width)

    line_boxes = [draw.textbbox((0, 0), line, font=font) for line in lines]
    max_ascent = max(-box[1] for box in line_boxes)
    line_heights = [(box[3] - box[1]) for box in line_boxes]

    text_block_width = max(box[2] - box[0] for box in line_boxes)
    text_block_height = sum(line_heights) + line_spacing * (len(lines) - 1)

    badge_width = text_block_width + 2 * padding
    badge_height = text_block_height + 2 * padding

    image = Image.new("RGBA", (int(badge_width), int(badge_height)), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        (0, 0, badge_width, badge_height),
        radius=border_radius,
        fill=background,
        outline=border_color,
        width=border_width,
    )

    y = padding + max_ascent

    for line, box, height in zip(lines, line_boxes, line_heights):
        text_width = box[2] - box[0]
        x = (badge_width - text_width) // 2

        draw.text((x, y), line, font=font, fill=foreground, align="center")

        y += height + line_spacing

    output_buffer = io.BytesIO()
    image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return output_buffer

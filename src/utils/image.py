import io
import math

import cairosvg
from PIL import Image


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

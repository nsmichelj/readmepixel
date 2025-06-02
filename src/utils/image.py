import io
import math

import cairosvg
from PIL import Image

from src.utils.conversion import svg_to_image


def create_skill_image(
    icons: list[str], icon_size: int, per_lines: int | None, spacing: int
):
    if not icons:
        skill_image = Image.new("RGBA", (icon_size, icon_size), "rgba(0, 0, 0, 0)")
        output_buffer = io.BytesIO()
        skill_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        return output_buffer

    num_icons = len(icons)

    if not per_lines or per_lines > num_icons or per_lines < 1:
        per_lines = num_icons

    rows = math.ceil(num_icons / per_lines)

    # Calculate total image dimensions
    total_width = (per_lines * icon_size) + (max(0, per_lines - 1) * spacing)
    total_height = (rows * icon_size) + (max(0, rows - 1) * spacing)

    skill_image = Image.new("RGBA", (total_width, total_height), "rgba(0, 0, 0, 0)")

    for i, icon in enumerate(icons):
        icon_image = svg_to_image(icon, icon_size)
        if icon_image is None:
            continue

        row = i // per_lines
        col = i % per_lines
        x_offset = col * (icon_size + spacing)
        y_offset = row * (icon_size + spacing)

        skill_image.paste(icon_image, (x_offset, y_offset), icon_image)

    output_buffer = io.BytesIO()
    skill_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return output_buffer

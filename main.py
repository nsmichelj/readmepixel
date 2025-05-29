import io
import math
from contextlib import asynccontextmanager

import cairosvg
from fastapi import FastAPI, Response
from PIL import Image

from src.utils.icons import get_icons, load_svgs


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_svgs()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/skills")
async def skill_image(
    icons: str = "html5,css,js",
    icon_size: int = 50,
    per_lines: int | None = None,
    spacing: int = 10,
):
    requested_icons = [icon.strip().lower() for icon in icons.split(",")]
    svg_icons_content = get_icons(requested_icons)
    num_icons = len(svg_icons_content)

    if not per_lines or per_lines > num_icons or per_lines < 1:
        per_lines = num_icons

    rows = math.ceil(num_icons / per_lines)

    # Calculate total image dimensions
    total_width = (per_lines * icon_size) + (max(0, per_lines - 1) * spacing)
    total_height = (rows * icon_size) + (max(0, rows - 1) * spacing)

    skill_image = Image.new("RGBA", (total_width, total_height), "rgba(0, 0, 0, 0)")

    for i, icon in enumerate(svg_icons_content):
        png_data = cairosvg.svg2png(
            bytestring=icon, output_width=icon_size, output_height=icon_size
        )  # type: ignore
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

    return Response(content=output_buffer.getvalue(), media_type="image/png")

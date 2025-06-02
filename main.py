from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

from src.utils.icons import get_icons, load_svgs
from src.utils.image import create_skill_image, create_badge_image


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
    output_buffer = create_skill_image(svg_icons_content, icon_size, per_lines, spacing)

    return Response(content=output_buffer.getvalue(), media_type="image/png")


@app.get("/badge")
async def badge_image(
    text: str,
    font_size: int = 14,
    padding: int = 10,
    line_spacing: int = 10,
    max_width: float | None = None,
    border_radius: int = 0,
    background: str = "#4A90E2",
    foreground: str = "white",
    border_color: str = "#00000000",  # Transparente por defecto (cambiado de "white")
    border_width: int = 2,
):
    output_buffer = create_badge_image(
        text,
        font_size,
        padding,
        line_spacing,
        max_width,
        border_radius,
        background,
        foreground,
        border_color,
        border_width,
    )

    return Response(content=output_buffer.getvalue(), media_type="image/png")

from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

from src.utils.icons import get_icons, load_svgs
from src.utils.image import create_skill_image


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

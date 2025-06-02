from PIL import Image
import io
import cairosvg
from typing import Optional


def svg_to_image(svg_data: str, size: int) -> Optional[Image.Image]:
    png_data = cairosvg.svg2png(
        bytestring=svg_data, output_width=size, output_height=size
    )
    if isinstance(png_data, bytes):
        return Image.open(io.BytesIO(png_data)).convert("RGBA")
    return None

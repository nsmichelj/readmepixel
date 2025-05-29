import os

ICONS_DIR = "static/icons"
ICONS_CACHE: dict[str, str] = {}


def normalize_name(name: str):
    return name.lower().replace(" ", "_").replace("-", "_")


def load_svgs():
    for filename in os.listdir(ICONS_DIR):
        if filename.endswith(".svg"):
            icon_name, _ = os.path.splitext(filename)
            with open(os.path.join(ICONS_DIR, filename), "r") as f:
                ICONS_CACHE[normalize_name(icon_name)] = f.read()


def get_icons(icons: list[str]):
    found_icons: list[str] = []
    for icon in icons:
        searched_icon = ICONS_CACHE.get(normalize_name(icon))
        if searched_icon:
            found_icons.append(searched_icon)

    return found_icons

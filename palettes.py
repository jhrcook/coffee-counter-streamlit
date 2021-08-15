"""Colors and color palettes."""
import random
from collections.abc import Sequence

bag_color_palette: dict[str, str] = {
    "Beyond Black": "#121212",
    "Coffee or Die": "#6B2121",
    "Escape Goat": "#3FEFAC",
    "Flying Elk": "#FFE94A",
    "Gunship": "silver",
    "Liberty": "red",
    "Magia del Campo": "#4ECE4E",
    "Mind, Body & Soul": "#BA2121",
    "Power Llama": "#3749A2",
    "Silencer Smooth": "#B8CCF2",
    "Space Bear": "#DE9153",
    "Tactisquatch": "#D8553A",
    "Blackbeard's Delight": "#7F2E28",
    "House Blend": "#2CADE1",
    "Seabright": "#B7CCF3",
    "Lava Panther": "#FA5A40",
}


def random_color() -> str:
    """Create a random color."""
    hexadecimal = "".join([random.choice("ABCDEF0123456789") for i in range(6)])
    return hexadecimal


def fill_in_missing_bags(pal: dict[str, str], bags: Sequence) -> dict[str, str]:
    """Fill in the colors for bags not in existing color palette.

    Args:
        pal (dict[str, str]): Existing color palette with [bag: color] format.
        bags (Sequence): Bags that should be included in the palette.

    Returns:
        dict[str, str]: Copy of the original palette with the new bags included.
    """
    new_pal = pal.copy()
    bags_with_colors = set(new_pal.keys())
    for bag in bags:
        if bag not in bags_with_colors:
            new_pal[bag] = random_color()
    return new_pal

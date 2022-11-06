#!/usr/bin/env python

from pathlib import Path
import random
import re
import pywal

ALACRITTY_CONFIG = Path.home() / Path(".config/alacritty/alacritty.yml")
THEMES_DIR = ALACRITTY_CONFIG.parent / Path("themes/")
THEME_TEXT = "~/.config/alacritty/themes/"  # Unique Pattern Inside alacritty config


def random_theme() -> str:
    """TODO: Docstring for random_theme.
    Returns: TODO

    """
    themes = [themes.stem for themes in THEMES_DIR.iterdir()]
    return themes[random.randint(0, len(themes) - 1)]


# Probably changed to random_path_item and merged with above
def random_wallpaper(wallpapers_dir: Path) -> Path:
    """TODO: Docstring for random_wallpaper.

    Args:
        wallpapers_dir (Path): A Path Directory

    Returns: A path for a single wallpaper

    """

    wallpapers = [x for x in wallpapers_dir.rglob("*.jpg")]
    return wallpapers[random.randint(0, len(wallpapers) - 1)]


def generate_pywall_theme(wallpaper: Path, template: Path, export_file: Path) -> None:
    """Docstring for generate_pywall_theme.
    Generate a Pywall theme based on Wallpaper and Pywall Template.

    Args:
        wallpaper (Path): TODO
        template (Path): Pywall Template locaiton
        export_file (Path): Pywall theme export locaiton

    Returns: None, Creates Pywall theme based on wall paper

    """
    image = pywal.image.get(wallpaper)
    colors = pywal.colors.get(image)
    # Should change this to save in cache and then cp over to correct location? Not sure if that actually fixes cache problem
    pywal.export.color(colors, template, export_file)


def regex_config(config: Path, new_pattern: str, old_pattern: str, **kwargs) -> None:
    """TODO: Docstring for regex_config.

    Updates the Config File based on Regex Pattern provided.

    Returns: None, but edits file destructively.

    """
    with config.open("r") as f:
        content = f.read()
        new_content = re.sub(old_pattern, new_pattern, content, **kwargs)

    with config.open("w") as f:
        f.write(new_content)


def main() -> None:
    """Main

    Update the Alacritty Config to A Random theme.

    Returns: None

    """
    # Set Regex patterns
    new_pattern = rf"\1pywall\3"
    old_pattern = rf"({THEME_TEXT})(.*)(.yml)"

    # Set Variables
    export_file = Path.home() / Path(".config/alacritty/themes/pywal.yml")
    template = Path.home() / Path(".config/wal/templates/colors-alacritty.yml")
    wallpapers_dir = Path.home() / Path("git_repos/dotfiles/wallpapers")

    # Randomly select a Wallpaper from dir
    wallpaper = random_wallpaper(wallpapers_dir)

    # Generate Pywall theme based on wallpaper
    generate_pywall_theme(wallpaper, template, export_file)
    _random = False if "dragon" in wallpaper.parts[-2].lower() else True

    if _random:
        # Get a Random Theme
        theme = random_theme()
        new_pattern = rf"\1{theme}\3"

    # Edit Alacritty config file
    regex_config(ALACRITTY_CONFIG, new_pattern, old_pattern, count=1)


if __name__ == "__main__":
    main()

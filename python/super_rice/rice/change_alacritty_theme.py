#!/usr/bin/env python

from pathlib import Path
import random
import re
import pywal

ALACRITTY_CONFIG = Path("~/.config/alacritty/alacritty.toml").expanduser()
ALACRITTY_COLOR_CONFIG = Path("~/.config/alacritty/theme_imports.toml").expanduser()
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
        wallpaper (Path): A Path to wallpaper
        template (Path): Pywall Template locaiton
        export_file (Path): Pywall theme export locaiton

    Returns: None, Creates Pywall theme based on wall paper

    """
    image = pywal.image.get(wallpaper)
    colors = pywal.colors.get(image)
    # Should change this to save in cache and then cp over to correct location? Not sure if that actually fixes cache problem
    pywal.export.color(colors, template, export_file)


def regex_config(
    config: Path,
    new_pattern: str,
    old_pattern: str,
    force_reload_config: bool = True,
    alacritty_config: Path = Path("~/.config/alacritty/alacritty.toml").expanduser(),
    **kwargs,
) -> None:
    """TODO: Docstring for regex_config.

    Updates the Config File based on Regex Pattern provided.

    Args:
        config (Path): A Path for a config file to be altered
        new_pattern (str): A string or regex to replace old_pattern
        old_pattern (str): A string or regex to be replaced

    Returns: None, but edits file destructively.

    """
    with config.open("r") as f:
        content = f.read()
        new_content = re.sub(old_pattern, new_pattern, content, **kwargs)

    with config.open("w") as f:
        f.write(new_content)

    if force_reload_config:
        force_reload_alacritty_config(alacritty_config)


def force_reload_alacritty_config(config: Path) -> None:
    """Docstring for force_reload_alacritty.

    Forces the Alacritty config to be reloaded. This works based on
    the fact that Alacritty autoreloads when it changes. This feature
    is intended to allow you to have a separate theming file that is
    updated with regex_config. Normally since that is a separate file
    Alacritty would not reload the config file. This function solves
    this problem by appending a blank line and then erasing it in the
    alacritty config file. This is not intended to allow you to reload
    alacritty without the live_config_reload: true option set in your
    config file.

    Args:
        config (Path): A Path for a config file to be altered

    Returns: None, just forces alacritty to reload the config

    """
    with config.open("r") as f:
        content = f.read()

    with config.open("w") as f:
        f.write(content + "\n")

    with config.open("w") as f:
        f.write(content)


def main(wallpaper: Path) -> None:
    """Main

    Update the Alacritty Config to A Random theme.

    Args:
        wallpaper (Path): A Path to wallpaper

    Returns: None

    """
    # Set Regex patterns
    new_pattern = rf"\1pywal\3"
    old_pattern = rf"({THEME_TEXT})(.*)(.toml)"

    # Set Variables
    export_file = Path("~/.config/alacritty/themes/pywal.toml").expanduser()
    template = Path("~/.config/wal/templates/colors-alacritty.toml").expanduser()
    wallpapers_dir = Path("~/git_repos/dotfiles/wallpapers").expanduser()

    # Randomly select a Wallpaper from dir
    if not wallpaper:
        wallpaper = random_wallpaper(wallpapers_dir)

    # Generate Pywall theme based on wallpaper
    generate_pywall_theme(wallpaper, template, export_file)
    _random = True if "dragon" in wallpaper.parts[-2].lower() else False

    if _random:
        # Get a Random Theme
        theme = random_theme()
        new_pattern = rf"\1{theme}\3"

    # Edit Alacritty config file
    regex_config(ALACRITTY_COLOR_CONFIG, new_pattern, old_pattern, count=1)


if __name__ == "__main__":
    wallpapers_dir = Path("~/git_repos/dotfiles/wallpapers").expanduser()
    wallpaper = random_wallpaper(wallpapers_dir)
    main(wallpaper)

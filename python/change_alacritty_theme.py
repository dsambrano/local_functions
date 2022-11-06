#!/usr/bin/env python

from pathlib import Path
import random
import re

ALACRITTY_CONFIG = Path.home() / Path(".config/alacritty/alacritty.yml")
THEMES_DIR = ALACRITTY_CONFIG.parent / Path("themes/")
THEME_TEXT = "~/.config/alacritty/themes/"  # Unique Pattern Inside alacritty config


def random_theme() -> str:
    """TODO: Docstring for random_theme.
    Returns: TODO

    """
    themes = [themes.stem for themes in THEMES_DIR.iterdir()]
    theme = themes[random.randint(0, len(themes) - 1)]
    return theme


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

    # Get a Random Theme
    theme = random_theme()

    # Set Regex patterns
    new_pattern = rf"\1{theme}\3"
    old_pattern = rf"({THEME_TEXT})(.*)(.yml)"

    # Edit Alacritty config file
    regex_config(ALACRITTY_CONFIG, new_pattern, old_pattern, count=1)


if __name__ == "__main__":
    main()

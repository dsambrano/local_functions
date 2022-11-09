#!/usr/bin/env python

from pathlib import Path
import random


# Probably changed to random_path_item and merged with above
def random_wallpaper(wallpapers_dir: Path) -> Path:
    """TODO: Docstring for random_wallpaper.

    Args:
        wallpapers_dir (Path): A Path Directory

    Returns: A path for a single wallpaper

    """

    wallpapers = [x for x in wallpapers_dir.rglob("*.jpg")]
    return wallpapers[random.randint(0, len(wallpapers) - 1)]


def main() -> None:
    """TODO: Docstring for main.

    Returns: A Riced Setup

    """

    wallpapers_dir = Path("~/git_repos/dotfiles/wallpapers").expanduser()

    # Randomly select a Wallpaper from dir
    wallpaper = random_wallpaper(wallpapers_dir)

    from rice import change_wallpaper

    change_wallpaper.main(wallpaper)
    os = change_wallpaper.get_os()
    change_wallpaper = change_wallpaper.get_wallpaper_function(os)
    change_wallpaper(wallpaper)

    # Running Second because of animation for wallpaper
    from rice import change_alacritty_theme

    change_alacritty_theme.main(wallpaper)


if __name__ == "__main__":
    main()

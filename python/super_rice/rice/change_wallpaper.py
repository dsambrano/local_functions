from pathlib import Path
import enum
import re
import subprocess
import sys

from pywal.wallpaper import change


class OS(enum.Enum):
    MAC = "MacOS"
    FEDORA = "Fedora Linux"


def get_os() -> OS:
    """TODO: Docstring for get_os.
    Returns: TODO

    """
    release = Path("/etc/os-release")
    with release.open("r") as f:
        content = f.read()

    long_os = re.match(r'NAME="(.*)"', content).groups()[0]
    os = OS(long_os)
    return os


def change_gnome_wallpaper(wallpaper: Path) -> None:
    """TODO: Docstring for change_gnome_wallpaper.

    Args:
        wallpaper (Path): A Path to a Wallpaper

    Returns: None Changes Gnome Wallpaper

    """
    preference_commands = [
        "gsettings",
        "get",
        "org.gnome.desktop.interface",
        "color-scheme",
    ]
    preference = subprocess.run(preference_commands, stdout=subprocess.PIPE, text=True)
    key = "picture-uri-dark" if "dark" in preference.stdout else "picture-uri"

    # Setting Scale for Wallpaper
    ##  values for picture-options: ‘none’, ‘wallpaper’, ‘centered’, ‘scaled’, ‘stretched’, ‘zoom’, ‘spanned’
    subprocess.run(
        [
            "gsettings",
            "set",
            "org.gnome.desktop.background",
            "picture-options",
            "'scaled'",
        ]
    )

    # Changing the Wallpaper
    wallpaper_commands = [
        "gsettings",
        "set",
        "org.gnome.desktop.background",
        key,
        wallpaper.as_uri(),
    ]
    subprocess.run(wallpaper_commands)


def change_macos_wallpaper(wallpaper: Path):
    """Changes Wallpaper for MacOS

    Args:
        wallpaper (Path): TODO

    Returns: TODO

    """
    pic = wallpaper.resolve().as_posix()
    wallpaper_commands = ["osascript", "-e"]
    commands_string = (
        f'tell application "Finder" to set desktop picture to POSIX file "{pic}"'
    )
    subprocess.run(wallpaper_commands, input=commands_string)


def get_wallpaper_function(os: OS) -> callable:
    """TODO: Docstring for get_wallpaper_function.

    Args:
        os (OS): An OS object

    Returns: Function to update the wallpaper

    """
    os_change_wallpaper = {
        OS.MAC.name: change_macos_wallpaper,
        OS.FEDORA.name: change_gnome_wallpaper,
    }
    return(os_change_wallpaper[os.name])


def main(wallpaper: Path):
    """TODO: Docstring for main.

    Args:
        wallpaper (Path): TODO

    Returns: TODO

    """
    os = get_os()
    change_wallpaper = get_wallpaper_function(os)
    change_wallpaper(wallpaper)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        wallpaper = Path(sys.argv[1]).expanduser()
    else:
        from change_alacritty_theme import random_wallpaper
        wallpapers_dir = Path("~/git_repos/dotfiles/wallpapers/").expanduser()
        wallpaper = random_wallpaper(wallpapers_dir)


    main(wallpaper)

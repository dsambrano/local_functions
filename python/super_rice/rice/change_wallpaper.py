from pathlib import Path
import enum
import re
import subprocess
import sys
import logging

from pywal.wallpaper import change

logging.basicConfig(level=logging.DEBUG, filename='/home/buddy/wallpaper.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt="%Y-%-m-%d %H:%M:%S")


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
    # Get current DE: https://tecadmin.net/detect-the-desktop-environment-in-linux-command-line/
    # echo $XDG_CURRENT_DESKTOP
    return os

def change_linux_wallpaper(wallpaper: Path) -> None:
    """change_linux_wallpaper
    Changes wallpaper for linux depending on DE. If you are using a Tiling 
    Window Manager (e.g., i3, awesome), then it will use feh. Otherwise, it 
    assumes you are using gnome, in which case it will use use gsettings for 
    your preferred color theme (light or dark).

    Args:
        wallpaper (Path): A Path to a Wallpaper

    Returns: None; Changes Wallpaper for Linux

    """
    window_managers = ["awesome", "i3"]
    wm_regex = "|".join(window_managers)
    commands = ["pgrep", wm_regex]
    wm_ps = subprocess.run(commands, stdout=subprocess.PIPE, text=True)

    if wm_ps.stdout:
        change_wm_wallpaper(wallpaper)
    else:
        change_gnome_wallpaper(wallpaper)


def change_wm_wallpaper(wallpaper: Path) -> None:
    """TODO: Docstring for change_wm_wallpaper.

    Args:
        wallpaper (Path): A Path to a Wallpaper

    Returns: None Changes Wallpaper For Tiling Window Mangagers using feh

    """
    # The problem was a lack of env in cron, I moved the content beelow to use the one line for exporting inside the crontab
    #  https://superuser.com/a/1038538
    # import os
    # os.environ["DISPLAY"] = ":0"
    # logging.warn(f"OS Vars: {os.getenv('DISPLAY')}")
    process = subprocess.run(["feh", "--bg-scale", str(wallpaper)], stdout=subprocess.PIPE)
    #output, error = process.communicate()
    logging.error(f"Output: {process}")
    # logging.error(f"Execption", exec_info=True)

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
        OS.FEDORA.name: change_linux_wallpaper,
    }
    return(os_change_wallpaper[os.name])


def main(wallpaper: Path):
    """TODO: Docstring for main.

    Args:
        wallpaper (Path): pathlib.Path file to be used a wallpaper

    Returns: None, Update the Wallpaper for MacOS of Linux

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

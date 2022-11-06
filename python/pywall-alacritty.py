from pathlib import Path
import sys
import pywal


WALLPAPER = Path.home() / Path("git_repos/dotfiles/wallpapers") / Path("generic/deer_sunset_blue.jpg")
if not WALLPAPER.exists():
    print("Typo you dunce")
    print(WALLPAPER)
    sys.exit()
image = pywal.image.get(WALLPAPER)
colors = pywal.colors.get(image)
pywal.export.color(colors, "/home/buddy/.config/wal/templates/colors-alacritty.yml", "/home/buddy/.config/alacritty/themes/pywal.yml")


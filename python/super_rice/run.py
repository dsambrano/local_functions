#!/usr/bin/env python3

import rice
from pathlib import Path
import os

if os.system("gprep i3lock") != 265:
    wallpapers_dir = Path("~/git_repos/dotfiles/wallpapers/").expanduser()
    rice.main(wallpapers_dir)

#!/usr/bin/env python3

import rice
from pathlib import Path

wallpapers_dir = Path("~/git_repos/dotfiles/wallpapers/").expanduser()

rice.main(wallpapers_dir)

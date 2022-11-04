#!/usr/bin/env bash


mkdir ~/.local/bin
export PATH="$HOME/.local/bin:$PATH"
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
# Could also use mv instead.
ln -s ~/git_repos/local_functions/shell/change_wallpaper.sh ~/.local/bin


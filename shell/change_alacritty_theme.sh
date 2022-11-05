#!/usr/bin/env bash


# Update the Alacritty theme
sed -i "s@\(themes/\)\(.*\)\(.yml\)@\1purples\3@" ~/.config/alacritty/alacritty.yml

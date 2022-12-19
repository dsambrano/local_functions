#!/usr/bin/env bash

#gsettings get org.gnome.desktop.background picture-uri
#'file:///usr/share/backgrounds/fedora-workstation/winter-in-bohemia.png'

#gsettings set org.gnome.desktop.background picture-uri ""

get_os() {
    OS=$(cat /etc/os-release | grep '^NAME' | grep -oP '"\K[^"\047]+(?=["\047])')
    echo $OS
}


change_gnome_wallpaper() {
    key="picture-uri"
    pref=$(gsettings get org.gnome.desktop.interface color-scheme)
    if [[ $pref == *"dark"* ]]
    then
        key="picture-uri-dark"
    fi

    # Adapted from https://www.roboleary.net/2021/09/02/linux-change-wallpaper.html 
    # values for picture-options: ‘none’, ‘wallpaper’, ‘centered’, ‘scaled’, ‘stretched’, ‘zoom’, ‘spanned’
    gsettings set org.gnome.desktop.background picture-options 'scaled'
    gsettings set org.gnome.desktop.background $key "file://$pic"
}

change_linux_wallpaper(){
    window_managers="awesome|i3" 
    if pgrep $window_managers>/dev/null; then
        feh --bg-scale $pic
    else
        change_gnome_wallpaper
    fi
}

change_macos_wallpaper() {
    # https://lifehacker.com/set-your-macs-wallpaper-with-a-terminal-command-1728551470
    # Needs to be checked to see if I can replace single quotes so I can expand param else will need to use eval probably.
    osascript -e 'tell application "Finder" to set desktop picture to POSIX file "$pic"'
}

main() {
    folder="${HOME}/git_repos/dotfiles/wallpapers"
    pic=$(find $folder/* | grep "jpg$" | shuf -n1)

    OS=$(get_os)
    case $OS in
        *"Fedora"*)
            change_linux_wallpaper;;
        *"Darwin"*)
            change_macos_wallpaper;;
    esac
}

main

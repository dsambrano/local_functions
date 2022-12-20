#!/usr/bin/env bash

# Taken from Dracula Tmux theme:

# Dracula Color Pallette
white='#f8f8f2'
gray='#44475a'
dark_gray='#282a36'
light_purple='#bd93f9'
dark_purple='#6272a4'
cyan='#8be9fd'
green='#50fa7b'
orange='#ffb86c'
red='#ff5555'
pink='#ff79c6'
yellow='#f1fa8c'

flags=""
current_flags=""

show_left_sep=$(get_tmux_option "@dracula-show-left-sep" )
show_right_sep=$(get_tmux_option "@dracula-show-right-sep" )

right_sep="$show_right_sep"
left_sep="$show_left_sep"

left_icon="session"

tmux_set_a(){
    # Set it Globally
    tmux set-option -ga $1 $2
    # For some reason during my testing, the global option doesnt work on active session
    tmux set-option -a $1 $2
}

tmux_set(){
    # Set it Globally
    tmux set-option -g $1 $2
    # For some reason during my testing, the global option doesnt work on active session
    tmux set-option $1 $2
}

tmux_set_window(){
    tmux set-window-option -g $1 $2
    tmux set-window-option $1 $2

# pane border styling
tmux_set pane-active-border-style "fg=${dark_purple}"
tmux_set pane-border-style "fg=${gray}"

# Msg Styling
tmux_set message-style "bg=${gray},fg=${white}"

# Status Bar
tmux_set status-style "bg=${gray},fg=${white}"

# Status Left
tmux_set status-left "#[bg=${green},fg=${dark_gray}]#{?client_prefix,#[bg=${yellow}],} ${left_icon} #[fg=${green},bg=${gray}]#{?client_prefix,#[fg=${yellow}],}${left_sep}"
powerbg=${gray}

# Staus Right
tmux_set_a status-right "#[fg=${!colors[0]},bg=${powerbg},nobold,nounderscore,noitalics]${right_sep}#[fg=${!colors[1]},bg=${!colors[0]}] $script "
powerbg=${!colors[0]}

# Window option
tmux_set_window window-status-current-format "#[fg=${gray},bg=${dark_purple}]${left_sep}#[fg=${white},bg=${dark_purple}] #I #W${current_flags} #[fg=${dark_purple},bg=${gray}]${left_sep}"

tmux_set_window window-status-format "#[fg=${white}]#[bg=${gray}] #I #W${flags}"

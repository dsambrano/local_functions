#!/usr/bin/env bash


# # 2>&1 redirected stderr to bin as well
# xdg-open "$1" > /dev/null &

open() { 
    # The () initializes a subshell preventing output and the disown
    # gives up ownership so you can close you terminal without affecting
    # the process
    (xdg-open "$@" &> /dev/null &; disown)
}


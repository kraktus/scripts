#!/usr/bin/env zsh

utils-git-current-branch() {
    ref=$(git symbolic-ref HEAD 2> /dev/null) || return
    echo ${ref#refs/heads/}
}

utils-confirm() {
    read -rk "REPLY?$1"
    [[ "$REPLY" == $'\n' ]]
}
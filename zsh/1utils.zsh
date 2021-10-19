#!/usr/bin/env zsh

# https://github.com/ohmyzsh/ohmyzsh/blob/12669f29f0843b8b980dd137f150a74511f88842/lib/git.zsh#L96
utils-git-current-branch() {
  local ref
  ref=$(git symbolic-ref --quiet HEAD 2> /dev/null)
  local ret=$?
  if [[ $ret != 0 ]]; then
    [[ $ret == 128 ]] && return  # no git repo.
    ref=$(git rev-parse --short HEAD 2> /dev/null) || return
  fi
  echo ${ref#refs/heads/}
}

utils-confirm() {
    read -rk "REPLY?>>> $1"
    [[ "$REPLY" == $'\n' ]]
}
#!/usr/bin/env zsh

# /!\ PUBLIC do NOT commit sensitive stuff (ssh pwd etc) /!\

export EDITOR='subl -w'

export HOMEBREW_NO_GOOGLE_ANALYTICS=true # https://brew.sh/2023/02/16/homebrew-4.0.0/

# https://zsh.sourceforge.io/Doc/Release/Options.html#Options
setopt AUTO_CD
setopt INC_APPEND_HISTORY # https://stackoverflow.com/a/45639156/11955835
setopt HIST_IGNORE_DUPS # https://unix.stackexchange.com/a/603977
setopt EXTENDED_HISTORY # https://linux.die.net/man/1/zshoptions
SAVEHIST=10000000

# enable auto-completion for brew added CLI: https://docs.brew.sh/Shell-Completion
if type brew &>/dev/null
then
  FPATH="$(brew --prefix)/share/zsh/site-functions:${FPATH}"

  autoload -Uz compinit
  compinit
fi

# aliases
for zsh_file (~/Github/scripts/zsh/*.zsh) source $zsh_file

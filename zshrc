#!/usr/bin/env zsh

# /!\ PUBLIC do NOT commit sensitive stuff (ssh pwd etc) /!\

export EDITOR='subl -w'

export LANG="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8" # see https://github.com/mobile-shell/mosh/issues/793


export PS1="MB1 %~ %# " # "context prompt" (first line of the terminal) COMMENTS BELOW
# see https://stackoverflow.com/questions/34623956/how-to-get-absolute-path-on-a-zsh-prompt
# Displays as "MB1 ~/full/path %". `%#` means A ‘#’ if the shell is running with privileges, a ‘%’ if not.
# from https://zsh.sourceforge.io/Doc/Release/Prompt-Expansion.html

# enable auto-completion for brew https://docs.brew.sh/Shell-Completion
eval "$(brew shellenv)"
autoload -Uz compinit
compinit

# for scala-cli
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
# for rails/gems 
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
export PATH="/opt/homebrew/lib/ruby/gems/3.4.0/bin:$PATH"

# https://zsh.sourceforge.io/Doc/Release/Options.html#Options
setopt AUTO_CD
setopt INC_APPEND_HISTORY # https://stackoverflow.com/a/45639156/11955835
setopt HIST_IGNORE_DUPS # https://unix.stackexchange.com/a/603977
setopt EXTENDED_HISTORY # https://linux.die.net/man/1/zshoptions
SAVEHIST=10000000

# Central shared cargo target directory, sharing builds of common dependencies across projects. 
# Although clearing it will clear artifacts from all projects
export CARGO_TARGET_DIR="$HOME/.cargo/target"

# aliases
for zsh_file (~/Github/scripts/zsh/*.zsh) source $zsh_file

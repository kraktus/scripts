#!/usr/bin/env zsh

# https://github.com/ornicar/dotfiles/tree/master/zsh
# https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git

# Never make an alias dependent of another one, only rename

alias g="git"
alias ga="git add -u" # Add all modified files if no args provided, otherwise only add the specified files
alias gaa="git add -A"
alias gb="git branch"
alias gc="git commit -v"
alias gd="git diff"
alias gp="git push"
alias gph="git pull head $(utils-git-current-branch) && git push"

# Shortcut for interactive rebase
gr(){
    git rebase -i HEAD~$1
}
alias gs="git status"
go() { # git checkout gitout gout go
    git checkout $1
    if (( $? )) # https://stackoverflow.com/a/43481571/11955835
    then
        if utils-confirm "No branch named $1, press ENTER to create it "
        then
            git checkout -b $1
        fi
    fi
}
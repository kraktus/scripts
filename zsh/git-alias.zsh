#!/usr/bin/env zsh

# https://github.com/ornicar/dotfiles/tree/master/zsh
# https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git

# Never make an alias dependent of another one, only rename

alias g="git"
ga(){  # Add all modified files if no args provided, otherwise only add the specified files
    if [ -z $@ ]
    then
        git add -u
    else
        git add $@
    fi
}
alias gaa="git add -A"
alias gac="git add -u && git commit -v"
alias gb="git branch"
alias gc="git commit -v"
alias gd="git diff"
gp() {
    git push $@
    if (( $? ))
    then
        if utils-confirm "Press ENTER to create the remote branch "
        then
            git push --set-upstream origin $(utils-git-current-branch)
        fi
    fi
}
alias gpf="git push -f"
alias gph="git pull head $(utils-git-current-branch) && git push"

# Shortcut for interactive rebase
gr(){
    git rebase -i HEAD~$1
}
alias gs="git status"
go() { # git checkout gitout gout go
    git checkout $@
    if (( $? ))
    then
        if utils-confirm "No branch named $1, press ENTER to create it "
        then
            git checkout -b $1
        fi
    fi
}
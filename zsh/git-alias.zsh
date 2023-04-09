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
alias gaac="git add -A && git commit -v"
alias gb="git branch"
alias gc="git commit -v"
# automatically concatenate the current unstaged changes to the last commit
g-concat() {
    git add -A && \
    git commit -a --allow-empty-message -m '' && \
    git reset --soft HEAD~2 && \
    git commit -v --edit -m"$(git log --format=%B --reverse HEAD..HEAD@{1})"
}
alias g-clean="git branch --merged | grep -v \* | xargs git branch -D"
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
gph(){
    echo "git pull head $(utils-git-current-branch) && git push"
    git pull head $(utils-git-current-branch) && git push
    if (( $? ))
    then
        echo "Error with remote head, trying origin"
        echo "git pull origin $(utils-git-current-branch) && git push"
        git pull origin $(utils-git-current-branch) && git push
    fi
}
g-pr(){
    git fetch head pull/$1/head:"pr-$1" --force && git checkout "pr-$1"
}

# Shortcut for interactive rebase
gr(){
    git rebase --committer-date-is-author-date -i HEAD~$1 # https://stackoverflow.com/a/2976598/11955835
}
alias grs="git restore"
alias grss="git restore --staged"
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
gom() {
    echo "git checkout master"
    git checkout master
    if (( $? ))
    then
        echo "No master branch, trying main"
        git checkout main
    fi
}
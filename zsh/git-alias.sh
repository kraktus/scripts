# https://github.com/ornicar/dotfiles/tree/master/zsh
# https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git

# Never make an alias dependent of another one, only rename

alias ga="git add -u"
alias gb="git branch"
alias gc="git commit -v"
alias gd="git diff"
alias gp="git push"
alias gph="git pull head master && git push"
# Shortcut for interactive rebase
gr(){
    git rebase -i HEAD~$1
}
alias gs="git status"
alias gout="git checkout"
alias goutb="git checkout -b"
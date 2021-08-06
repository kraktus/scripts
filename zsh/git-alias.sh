# https://github.com/ornicar/dotfiles/tree/master/zsh
# https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git

# Never make an alias dependent of another one, only rename

alias gita="git add -u"
alias gitb="git branch"
alias gitc="git commit -v"
alias gitd="git diff"
alias gitp="git push"
alias gitph="git pull head master && git push"
# Shortcut for interactive rebase
gitr(){
    git rebase -i HEAD~$1
}
alias gits="git status"
alias gitout="git checkout"
alias gitoutb="git checkout -b"
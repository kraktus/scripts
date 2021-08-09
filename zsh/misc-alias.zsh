#!/usr/bin/env zsh

# /!\ PUBLIC do NOT commit sensitive stuff (ssh pwd etc) /!\

# Never make an alias dependent of another one, only rename

setopt INC_APPEND_HISTORY # https://stackoverflow.com/a/45639156/11955835

alias dea="deactivate"
alias ls="ls -Gp"
# https://github.com/romkatv/powerlevel10k#weird-things-happen-after-typing-source-zshrc
# https://stackoverflow.com/questions/56284264/recommended-method-for-reloading-zshrc-source-vs-exec#56303297
# With exec, all (unexported) variables in your shell are lost
alias modif="subl --new-window --wait ~/Github/scripts/zsh/* ~/Github/scripts/zsh && exec zsh"
alias modif-p="subl --wait ~/.zshrc && exec zsh"
alias mongo="mongosh"
alias profile="python3 -m cProfile -s tottime"
alias py="python"
alias py3="python3"
venv(){
    source venv/bin/activate
    if (( $? )) # https://stackoverflow.com/a/43481571/11955835
    then
        echo "No venv found, creating one..."
        python3 -m venv venv
        source venv/bin/activate
    fi
}
alias ..="cd .."
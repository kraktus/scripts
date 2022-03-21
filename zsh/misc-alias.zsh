#!/usr/bin/env zsh

# /!\ PUBLIC do NOT commit sensitive stuff (ssh pwd etc) /!\

# Never make an alias dependent of another one, only rename

alias cch="cargo check"
alias cr="cargo run"
alias crr="cargo run --release"
alias ct="cargo test"
alias dea="deactivate"
alias ls="ls -Gp"
# https://github.com/romkatv/powerlevel10k#weird-things-happen-after-typing-source-zshrc
# https://stackoverflow.com/questions/56284264/recommended-method-for-reloading-zshrc-source-vs-exec#56303297
# With exec, all (unexported) variables in your shell are lost
alias modif="subl --new-window --wait ~/Github/scripts/zsh/* ~/Github/scripts && exec zsh" # https://github.com/sublimehq/sublime_text/issues/4740
alias modif-p="subl --wait ~/.zshrc && exec zsh"
alias mongo="mongosh"
alias path="realpath"
alias profile="python3 -m cProfile -s tottime"
alias pip='echo "USING PIP3" && pip3'
pip3(){
    if [[ "$1" == "install" ]]
    then
        if [ -z "$VIRTUAL_ENV" ]
        then
            echo "Not running in a venv, ABORTING"
        else
            python3 -m pip $@
        fi
    else
        python3 -m pip $@
    fi
} 
alias py="python"
alias py3="python3"
s(){
    local project="$(ls | grep .sublime-project)"
    if [ -z $@ ]
    then
        if [ -z "${project}" ] # check if empty string https://stackoverflow.com/questions/21274178/how-to-check-for-empty-string-in-ksh#21279027
        then
            echo "No Sublime Project found"
            subl .
        else
            echo "Sublime Project: $project found"
            subl --project "$project"
        fi
    else
        subl $@
    fi
}
venv(){
    source venv/bin/activate
    if (( $? )) # https://stackoverflow.com/a/43481571/11955835
    then
        echo "No venv found, creating one..."
        python3 -m venv venv --upgrade-deps # thanks 3.9
        source venv/bin/activate
    fi
}
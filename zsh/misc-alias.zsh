#!/usr/bin/env zsh

# /!\ PUBLIC do NOT commit sensitive stuff (ssh pwd etc) /!\

# Never make an alias dependent of another one, only rename

alias clippy-loc="~/Github/rust-clippy/target/debug/cargo-clippy"
alias dea="deactivate"
alias del-venv="rm -rf venv/"
alias lg="lazygit"
alias ls="ls -Gp"
# https://github.com/romkatv/powerlevel10k#weird-things-happen-after-typing-source-zshrc
# https://stackoverflow.com/questions/56284264/recommended-method-for-reloading-zshrc-source-vs-exec#56303297
# With exec, all (unexported) variables in your shell are lost
alias modif="subl --new-window --wait ~/Github/scripts/zsh/* ~/Github/scripts && exec zsh" # https://github.com/sublimehq/sublime_text/issues/4740
alias modif-p="subl --wait ~/.zshrc && exec zsh"
alias modif-ssh="subl --wait ~/.ssh/config && exec zsh"
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
alias ssh-keygen="ssh-keygen -t ed25519 -C Sol"
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
alias s-h="subl ~/.zsh_history"
venv(){
    source venv/bin/activate
    if (( $? )) # https://stackoverflow.com/a/43481571/11955835
    then
        echo "No venv found, creating one..."
        python3 -m venv venv --upgrade-deps # thanks 3.9
        source venv/bin/activate
    fi
}
# watermark image.png "Watermark Text"
watermark(){
    local IMAGE="$1"
    if [ ! -f "$IMAGE" ]; then
        echo "File not found!"
        return 1
    fi
    if [ -z "$2" ]; then
        echo "Usage: watermark <image> <watermark text>"
        return 1
    fi
    if ! command -v magick &> /dev/null
    then
        echo "ImageMagick not found, please install it first."
        return 1
    fi
    # get file without extension
    local FILENAME=$(basename "$IMAGE")
    local IMAGE_EXT="${FILENAME##*.}"
    local WATERMARK_TEXT="$2"
    # https://usage.imagemagick.org/annotating/#watermarking
      magick -size 600x450 xc:none -fill "rgba(255,0,0,0.4)" \
          -gravity center -pointsize 100 -draw "rotate -45 text 10,10 '$WATERMARK_TEXT'" \
          miff:- |\
    magick composite -tile - "$IMAGE"  "${FILENAME}_watermarked.${IMAGE_EXT}"
}
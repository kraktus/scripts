#!/usr/bin/env bash

# /!\ PUBLIC do NOT commit sensitive stuff (ssh pwd etc) /!\

# Never make an alias dependent of another one, only rename

alias c="cargo"
# alias cf="cargo fmt && taplo fmt --config ~/Github/scripts/.taplo.toml"
cf() {
    cargo fmt
    if (( $? ))
    then 
        fmt_0=false
    else
        fmt_0=true
    fi

	if [[ $(git remote) =~ "head" ]]
    then
        no_head=false
    else
        no_head=true
    fi

	if (( $fmt_0 && $no_head ))
    then
        taplo fmt --config ~/Github/scripts/.taplo.toml
    fi
}
alias ch="cargo check"
alias cr="cargo run"
alias crr="cargo run --release"
alias ct="cargo test"
#!/bin/sh

# https://github.com/ornicar/dotfiles/blob/63ab6477dc9f3975882e0bc273b7d0b0dd789ba2/scripts/install-link

# Absolute path to this script
SCRIPT=`realpath $0`
# Absolute path this script is in
SCRIPTPATH=`dirname $SCRIPT`
SUBLIME_PATH="~/Library/Application\ Support/Sublime\ Text/Packages/User"

echo "Linking config files from $SCRIPTPATH"

link (){
    FROM="$SCRIPTPATH/$1"
    TO=$2

    printf "ln -s %s %s\n" $FROM $TO

    rm -i $TO
    ln -s $FROM $TO
}


#link gitconfig ~/.gitconfig
#link gitignore_global ~/.gitignore_global
#link Sublime/Preferences.sublime-settings "$SUBLIME_PATH/Preferences.sublime-settings"
#link Sublime/py-template.sublime-snippet "$SUBLIME_PATH/py-template.sublime-snippet"
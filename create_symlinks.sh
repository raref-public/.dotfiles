#!/bin/bash
for file in tmux.conf vimrc .zprofile .bash_profile remmina; do ln -s $HOME/path/to/repo/$file $HOME/.$file; done

#!/bin/bash

NOW=`date +%Y-%m-%d\ %H:%M`

yaourt -Q > $HOME/.dotfiles/pkg.list
git --git-dir $HOME/.dotfiles/.git/ --work-tree=$HOME/.dotfiles add -A $HOME/.dotfiles/
git --git-dir $HOME/.dotfiles/.git/ --work-tree=$HOME/.dotfiles commit -a -m "$NOW update"
git --git-dir $HOME/.dotfiles/.git/ --work-tree=$HOME/.dotfiles status
git --git-dir $HOME/.dotfiles/.git/ --work-tree=$HOME/.dotfiles push -u origin master
yaourt -Syua
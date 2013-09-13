#!/bin/bash

DATE=`date +%Y-%m-%d`

yaourt -Q > $HOME/.dotfiles/pkg.list
git --git-dir $HOME/.dotfiles/.git/ --work-tree=$HOME/.dotfiles add -A $HOME/.dotfiles/
git --git-dir $HOME/.dotfiles/.git/ --work-tree=$HOME/.dotfiles commit -a -m "$DATE Update"
git --git-dir $HOME/.dotfiles/.git/ status
git --git-dir $HOME/.dotfiles/.git/ --work-tree=$HOME/.dotfiles push -u origin master
#yaourt -Syua

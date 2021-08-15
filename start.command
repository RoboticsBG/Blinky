#!/bin/bash
export PATH="/usr/local/sbin:$PATH"
eval "$(pyenv init -)"
pyenv shell 3.9.1
cd ~/Downloads/Blinky
python Blinky.py

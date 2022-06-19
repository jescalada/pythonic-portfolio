#!/bin/bash

tmux kill-server || echo "There are no servers currently running."
cd ~/pythonic-portfolio
git fetch && git reset origin/master --hard
source python3-virtualenv/bin/activate
pip3 install -r requirements.txt
tmux new-session -d -s pythonic-portfolio 'source python3-virtualenv/bin/activate && flask run --host=0.0.0.0'

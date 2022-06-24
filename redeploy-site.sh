#!/bin/bash

cd ~/pythonic-portfolio
git fetch && git reset origin/master --hard
source python3-virtualenv/bin/activate
pip3 install -r requirements.txt
systemctl restart myportfolio

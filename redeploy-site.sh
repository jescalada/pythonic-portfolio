#!/bin/bash

cd ~/pythonic-portfolio
git fetch && git reset origin/master --hard
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build

#!/bin/bash

sudo apt-get update > /dev/null

sudo apt-get -yq install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev rsync lsyncd > /dev/null

sudo mkdir -p /builds
sudo touch /etc/rsyncd.conf
sudo tee -a /etc/rsyncd.conf << 'EOF'
[splunklogs]
path = /builds
read only = false
EOF
sudo rsync --daemon

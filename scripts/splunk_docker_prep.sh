#!/bin/bash

sudo apt-get update > /dev/null

sudo apt-get -yq install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev > /dev/null
#
#sudo usermod -u 1000 splunk
#sudo groupmod -g 1000 splunk
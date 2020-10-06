#!/bin/bash

set -x
set -e

apt-get update > /dev/null
apt-get -yq install curl gnupg > /dev/null
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" | tee -a /etc/apt/sources.list.d/google-chrome.list
apt-get update > /dev/null
apt-get -yq install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev docker.io libbz2-dev unzip xvfb libxi6 libgconf-2-4 google-chrome-stable=85.0.4183.121-1 > /dev/null

curl -O https://www.python.org/ftp/python/3.8.2/Python-3.8.2.tar.xz
tar -xf Python-3.8.2.tar.xz
cd Python-3.8.2
./configure
make -j 4
make install
cd ..
pip3 install --upgrade pip wheel
pip3 install -r requirements.txt > /dev/null

wget https://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver

rm -rf ${CI_PROJECT_DIR}/artifacts/screenshots/
rm -rf ${CI_PROJECT_DIR}/artifacts/results/

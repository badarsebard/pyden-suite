#!/bin/bash

set -x

apt-get update > /dev/null
apt-get -yq install curl gnupg > /dev/null
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" | tee -a /etc/apt/sources.list.d/google-chrome.list
apt-get update > /dev/null
apt-get -yq install docker.io libbz2-dev python3 python3-pip unzip xvfb libxi6 libgconf-2-4 google-chrome-stable > /dev/null

pip3 install -r requirements.txt > /dev/null

wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver

rm -rf ${CI_PROJECT_DIR}/artifacts/screenshots/
rm -rf ${CI_PROJECT_DIR}/artifacts/results/

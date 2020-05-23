#!/usr/bin/env bash

set -x

echo "Downloading Splunk"
wget -O splunk-7.3.5-86fd62efc3d7-linux-2.6-amd64.deb 'https://www.splunk.com/page/download_track?file=7.3.5/linux/splunk-7.3.5-86fd62efc3d7-linux-2.6-amd64.deb&ac=&wget=true&name=wget&platform=Linux&architecture=x86_64&version=7.3.5&product=splunk&typed=release' &> /dev/null
# wget -O splunk-8.0.4-767223ac207f-linux-2.6-amd64.deb 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=8.0.4&product=splunk&filename=splunk-8.0.4-767223ac207f-linux-2.6-amd64.deb&wget=true'&> /dev/null

echo "Download complete. Installing..."
sudo dpkg -i splunk-7.3.5-86fd62efc3d7-linux-2.6-amd64.deb

sudo timedatectl set-timezone America/New_York
sudo -u splunk cp /home/vagrant/.bashrc ${SPLUNK_HOME}/.bashrc
sudo -u splunk cp /home/vagrant/.profile ${SPLUNK_HOME}/.profile
echo "alias splunk=${SPLUNK_BIN}" | sudo tee -a ${SPLUNK_HOME}/.bashrc > /dev/null
echo "splunk:${SPLUNK_PASS}" | sudo chpasswd
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -yq ntpdate build-essential libffi-dev libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev uuid-dev
sudo ntpdate ntp.ubuntu.com
cat << EOF | sudo -u splunk tee -a ${SPLUNK_HOME}/etc/system/local/user-seed.conf
[user_info]
USERNAME = admin
PASSWORD = ${SPLUNK_PASS}
EOF
sudo -u splunk tee -a ${SPLUNK_HOME}/etc/log-local.cfg << 'EOF'
[python]
splunk.pyden = DEBUG
EOF
sudo -u splunk tee -a ${SPLUNK_HOME}/bin/python_splunk.sh << 'EOF'
#!/bin/bash
"$(dirname "$0")/splunk" cmd python "$@"
EOF
sudo -u splunk chmod +x ${SPLUNK_HOME}/bin/python_splunk.sh
sudo -u splunk touch ${SPLUNK_HOME}/etc/.ui_login
sudo -i -u splunk ${SPLUNK_BIN} start --accept-license --no-prompt &> /dev/null

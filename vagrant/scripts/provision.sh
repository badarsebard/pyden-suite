#!/usr/bin/env bash

set -x

wget -O splunk-7.3.5-86fd62efc3d7-linux-2.6-amd64.deb 'https://www.splunk.com/page/download_track?file=7.3.5/linux/splunk-7.3.5-86fd62efc3d7-linux-2.6-amd64.deb&ac=&wget=true&name=wget&platform=Linux&architecture=x86_64&version=7.3.5&product=splunk&typed=release'
sudo dpkg -i /vagrant/splunk-7.3.5-86fd62efc3d7-linux-2.6-amd64.deb

sudo timedatectl set-timezone America/New_York
sudo -u splunk cp /home/vagrant/.bashrc ${SPLUNK_HOME}/.bashrc
sudo -u splunk cp /home/vagrant/.profile ${SPLUNK_HOME}/.profile
echo "alias splunk=${SPLUNK_BIN}" | sudo tee -a ${SPLUNK_HOME}/.bashrc > /dev/null
echo "splunk:${SPLUNK_PASS}" | sudo chpasswd
sudo apt-get install -yq sshpass build-essential libffi-dev libssl-dev
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
sudo -i -u splunk ${SPLUNK_BIN} start --accept-license --no-prompt

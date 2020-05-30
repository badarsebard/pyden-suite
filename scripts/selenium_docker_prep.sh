set -x

apt-get update
apt-get -yq install curl gnupg
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" | tee -a /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get -yq install libbz2-dev python3 python3-pip unzip xvfb libxi6 libgconf-2-4 google-chrome-stable

pip3 install -r requirements.txt

wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver

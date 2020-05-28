sudo apt-get update

sudo apt-get -yq install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev

sudo mkdir -p /opt/splunk/etc/apps/splunk_instrumentation/local
sudo touch /opt/splunk/etc/apps/splunk_instrumentation/local/user-prefs.conf
sudo tee -a /opt/splunk/etc/apps/splunk_instrumentation/local/user-prefs.conf << 'EOF'
[general]
render_version_messages = 0
hideInstrumentationOptInModal = 1
dismissedInstrumentationOptInVersion = 3
notification_python_3_impact = false
[general_default]
hideInstrumentationOptInModal = 1
showWhatsNew = 0
dismissedInstrumentationOptInVersion = 3
notification_python_3_impact = false
EOF
sudo touch /opt/splunk/etc/apps/splunk_instrumentation/local/telemetry.conf
sudo tee -a /opt/splunk/etc/apps/splunk_instrumentation/local/telemetry.conf << 'EOF'
[general]
optInVersionAcknowledged = 3
showOptInModal = 0
EOF
sudo chown splunk: /opt/splunk/etc/apps/splunk_instrumentation/local/user-prefs.conf

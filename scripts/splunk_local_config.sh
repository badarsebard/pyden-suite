#!/bin/bash

touch /opt/splunk/etc/system/local/user-prefs.conf
chown splunk: /opt/splunk/etc/system/local/user-prefs.conf
tee -a /opt/splunk/etc/system/local/user-prefs.conf << 'EOF'
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
touch /opt/splunk/etc/system/local/telemetry.conf
chown splunk: /opt/splunk/etc/system/local/telemetry.conf
tee -a /opt/splunk/etc/system/local/telemetry.conf << 'EOF'
[general]
optInVersionAcknowledged = 3
showOptInModal = 0
EOF
mkdir -p /opt/splunk/etc/apps/pyden-manager/local/
touch /opt/splunk/etc/apps/pyden-manager/local/app.conf
chown splunk: /opt/splunk/etc/apps/pyden-manager/local/app.conf
tee -a /opt/splunk/etc/apps/pyden-manager/local/app.conf << 'EOF'
[install]
is_configured = 1
EOF
touch /opt/splunk/etc/apps/pyden-manager/local/pyden.conf
chown splunk: /opt/splunk/etc/apps/pyden-manager/local/pyden.conf
tee -a /opt/splunk/etc/apps/pyden-manager/local/pyden.conf << 'EOF'
[appsettings]
EOF

ln -s /opt/splunk/var/log/splunk /builds/splunk-logs

/opt/splunk/bin/splunk restart -f --answer-yes --accept-license

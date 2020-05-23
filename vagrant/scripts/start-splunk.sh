#!/usr/bin/env bash

sudo ntpdate ntp.ubuntu.com
status=`sudo -u splunk ${SPLUNK_BIN} status`

echo "Splunk status is: $status"

if [[ "$status" == *"not running"* ]]; then
    echo Splunk was not running
    sudo -u splunk ${SPLUNK_BIN} start
else
    echo Splunk is running
fi

#!/bin/bash

# set SPLUNK_CREDS to user:password in order to use this script
find src -type d -exec chmod 0755 {} +
find src -type f -exec chmod 0644 {} +
tar --exclude 'pyden/local' -czvf pyden.tgz -C src pyden
tar --exclude='pyden-manager/local*' --exclude='pyden-manager/bin/build' --exclude='pyden-manager/bin/__pycache__' --exclude='pyden-manager/metadata/local.meta' --exclude='*.pyc' -czvf pyden-manager.tgz -C src pyden-manager
scripts/submit-app.sh pyden
pyden_failures=$(echo $?)
scripts/submit-app.sh pyden-manager
manager_failures=$(echo $?)
x=$(( $pyden_failures + $manager_failures ))
if [[ $x -gt 0 ]]
then
  echo "There were $x failures in apps."
  exit 1
else
  echo "Success"
fi
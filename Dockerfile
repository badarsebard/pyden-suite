FROM splunk/splunk:7.3

COPY src/pyden /opt/splunk/etc/apps/pyden
COPY src/pyden-manager /opt/splunk/etc/apps/pyden-manager
COPY src/pyden-examples /opt/splunk/etc/apps/pyden-examples
COPY scripts/packages.sh ./packages.sh
COPY scripts/selenium.sh ./selenium.sh
COPY test/test.py ./test.py

RUN ./packages.sh
RUN ./selenium.sh

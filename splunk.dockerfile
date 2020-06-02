FROM splunk/splunk:7.3

COPY src/pyden /opt/splunk/etc/apps/pyden
COPY src/pyden-manager /opt/splunk/etc/apps/pyden-manager
COPY src/pyden-examples /opt/splunk/etc/apps/pyden-examples
COPY scripts/splunk_docker_prep.sh ./splunk_docker_prep.sh
COPY scripts/splunk_local_config.sh /sbin/splunk_local_config.sh
COPY scripts/splunk_ansible_prep.yml /tmp/splunk_ansible_prep.yml

RUN ./splunk_docker_prep.sh

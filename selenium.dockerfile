FROM debian:buster-slim

COPY scripts/selenium_docker_prep.sh ./selenium_docker_prep.sh
COPY requirements.txt ./requirements.txt
RUN ./selenium_docker_prep.sh

FROM debian:buster-slim

COPY scripts/selenium_docker_prep.sh ./selenium_docker_prep.sh
RUN ./selenium_docker_prep.sh

ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN dnf install -y python3 && dnf clean all
COPY pi.py /opt/azl-tests/pi.py

ARG BASE_IMAGE
FROM ${BASE_IMAGE}

RUN dnf install -y telegraf && dnf clean all
COPY configs/telegraf.conf /etc/telegraf/telegraf.conf

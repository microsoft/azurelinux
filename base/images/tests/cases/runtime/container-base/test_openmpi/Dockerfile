ARG BASE_IMAGE
FROM ${BASE_IMAGE}

RUN dnf install -y openmpi openmpi-devel gcc && dnf clean all
COPY send_receive.c /opt/mpi-tests/send_receive.c

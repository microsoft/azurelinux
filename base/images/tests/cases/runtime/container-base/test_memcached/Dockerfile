ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN dnf install -y memcached nmap-ncat && dnf clean all
EXPOSE 11211

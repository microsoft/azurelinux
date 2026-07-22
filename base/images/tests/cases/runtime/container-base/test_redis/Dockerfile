ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN dnf install -y valkey-compat-redis && dnf clean all
EXPOSE 6379

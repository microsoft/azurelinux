ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN dnf install -y postgresql-server postgresql && dnf clean all
EXPOSE 5432

ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN dnf install -y nodejs curl && dnf clean all
COPY server.js /app/server.js
COPY response.txt /app/response.txt
EXPOSE 8080

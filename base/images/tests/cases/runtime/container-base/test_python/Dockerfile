ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN dnf install -y python3 curl && dnf clean all
COPY app.py /app/app.py
COPY response.txt /app/response.txt
EXPOSE 8080

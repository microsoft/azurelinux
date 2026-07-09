ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN dnf install -y ruby curl && dnf clean all
COPY app.rb /app/app.rb
COPY response.txt /app/response.txt
EXPOSE 8080

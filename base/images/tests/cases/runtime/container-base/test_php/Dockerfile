ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN dnf install -y php-cli php-pecl-zip unzip curl && dnf clean all
COPY router.php /app/router.php
COPY response.txt /app/response.txt
EXPOSE 8080

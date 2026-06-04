ARG BASE_IMAGE
FROM ${BASE_IMAGE}
RUN dnf install -y nginx curl && dnf clean all
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80

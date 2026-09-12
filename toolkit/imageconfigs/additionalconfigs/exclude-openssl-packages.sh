#!/bin/env bash
# Exclude openssl packages from dnf so it will always choose the openssl-compat packages.
cat >> /etc/dnf/dnf.conf << EOF
exclude=openssl openssl-libs openssl-devel openssl-static openssl-perl openssl-debuginfo
EOF

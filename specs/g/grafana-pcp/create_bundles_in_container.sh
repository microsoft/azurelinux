#!/bin/bash -eu
#
# create vendor and webpack bundles inside a container (for reproducibility)
# using a Go cache:
#   ./create_bundles_in_container.sh --security-opt label=disable -v $(pwd)/.gocache:/root/go
#

cat <<EOF | podman build -t grafana-pcp-build -f - .
FROM fedora:36

RUN dnf upgrade -y && \
    dnf install -y rpmdevtools python3-packaging make golang nodejs yarnpkg golang-github-jsonnet-bundler golang-github-google-jsonnet

WORKDIR /tmp/grafana-pcp-build
COPY grafana-pcp.spec create_bundles.sh build_frontend.sh list_bundled_nodejs_packages.py *.patch .
RUN mkdir bundles
CMD ./create_bundles.sh && mv *.tar.* bundles
EOF

podman run --name grafana-pcp-build --replace "$@" grafana-pcp-build
podman cp grafana-pcp-build:bundles/. .

#!/bin/bash -eu

# Revert upstream change: "rename plugin IDs from pcp-*-* to performancecopilot-*-*"
# https://github.com/performancecopilot/grafana-pcp/commit/70ca5cc307e231cea14281e1cd2268ae4f1f445c
# This change would break all existing custom dashboards. Using sed here instead of a patch
# to catch all future usage of the new upstream plugin ids.
find src cypress \( -name '*.ts' -o -name '*.json' -o -name '*.jsonnet' -o -name '*.libsonnet' \) \
  -exec sed -i \
  -e 's/performancecopilot-redis-datasource/pcp-redis-datasource/g' \
  -e 's/performancecopilot-vector-datasource/pcp-vector-datasource/g' \
  -e 's/performancecopilot-bpftrace-datasource/pcp-bpftrace-datasource/g' \
  -e 's/performancecopilot-flamegraph-panel/pcp-flamegraph-panel/g' \
  -e 's/performancecopilot-breadcrumbs-panel/pcp-breadcrumbs-panel/g' \
  -e 's/performancecopilot-troubleshooting-panel/pcp-troubleshooting-panel/g' \
  {} \;

# Build the frontend
yarn run build

# Build the dashboards
make build-dashboards

# Fix permissions (webpack sometimes outputs files with mode = 666 due to reasons unknown (race condition/umask issue afaics))
chmod -R g-w,o-w dist

#!/usr/bin/env bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

ENABLE_TELEMETRY="${ENABLE_TELEMETRY:-true}"

# Check if --disable-telemetry flag is present in arguments
for arg in "$@"; do
    if [[ "$arg" == "--disable-telemetry" ]]; then
        ENABLE_TELEMETRY=false
        break
    fi
done

# Start telemetry service if enabled and connection string is set
if [[ "$ENABLE_TELEMETRY" == "true" ]] && [[ -n "$AZURE_MONITOR_CONNECTION_STRING" ]]; then

    export OTEL_PORT=4317
    export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"
    export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:${OTEL_PORT}"
    
    /opt/telemetry-venv/bin/python /usr/local/bin/telemetry_hopper.py --port $OTEL_PORT > /var/log/image_customizer_telemetry.log 2>&1 || true &
    sleep 1
fi

exec "$@"

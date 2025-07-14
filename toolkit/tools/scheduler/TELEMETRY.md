# OpenTelemetry Instrumentation for Azure Linux Toolkit Scheduler

This document describes the OpenTelemetry instrumentation that has been added to the Azure Linux Toolkit scheduler to enable telemetry collection.

## Overview

The scheduler has been instrumented with OpenTelemetry to provide observability into:
- Overall build graph execution
- Individual package builds and tests
- Worker utilization
- Build failures and successes
- License checking operations

## Configuration

### Environment Variables

The telemetry system can be configured using standard OpenTelemetry environment variables:

- `OTEL_EXPORTER_OTLP_ENDPOINT`: The OTLP collector endpoint (e.g., `http://localhost:4317`)
- `OTEL_SDK_DISABLED`: Set to `"true"` to disable telemetry completely

### Command Line Flags

The scheduler also supports telemetry-specific command line flags:

- `--enable-telemetry`: Explicitly enable OpenTelemetry tracing
- `--otlp-endpoint`: Specify the OTLP collector endpoint

## Usage

### Basic Usage

To enable telemetry, you have several options:

1. **Using environment variables:**
   ```bash
   export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
   ./scheduler [other args...]
   ```

2. **Using command line flags:**
   ```bash
   ./scheduler --enable-telemetry --otlp-endpoint=http://localhost:4317 [other args...]
   ```

3. **Auto-detection:**
   If the `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable is set, telemetry will be automatically enabled.

### Setting up an OTLP Collector

You can use any OpenTelemetry-compatible collector. Here's an example using Jaeger:

```bash
# Run Jaeger with OTLP support
docker run -d --name jaeger \
  -p 16686:16686 \
  -p 14250:14250 \
  -p 4317:4317 \
  jaegertracing/all-in-one:latest
```

Then run the scheduler:
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
./scheduler [other args...]
```

## Telemetry Data

### Traces

The instrumentation creates the following types of spans:

1. **`scheduler.main`**: The root span for the entire scheduler execution
   - Attributes: scheduler version, worker count, build agent type

2. **`scheduler.build_graph`**: Span for the entire build graph execution
   - Attributes: node count, worker count, build attempts, configuration flags

3. **`scheduler.worker`**: Span for each worker thread

4. **`scheduler.build.{type}`**: Spans for individual package builds
   - Types: `LocalBuild`, `Test`, `RemoteRun`, etc.
   - Attributes: package name, type, architecture, cache usage, attempt number

5. **`scheduler.license_check`**: Spans for license checking operations
   - Attributes: package name

### Attributes

Common attributes included in spans:

- `package.name`: The friendly name of the package
- `package.type`: The type of package node (LocalBuild, Test, etc.)
- `package.architecture`: The target architecture
- `build.success`: Whether the build succeeded
- `build.error`: Error message if the build failed
- `build.attempt`: Which attempt this build represents
- `build.files_built_count`: Number of files built
- `test.success`: Whether tests passed
- `license.has_warnings`: Whether license warnings were found
- `license.has_errors`: Whether license errors were found

### Events

The instrumentation adds events for significant operations:
- Build request processing
- Build result completion
- Error conditions

## Implementation Details

### Files Modified

1. **`internal/telemetry/telemetry.go`**: Core telemetry infrastructure
2. **`scheduler/schedulerutils/telemetry.go`**: Scheduler-specific telemetry utilities
3. **`scheduler/scheduler.go`**: Main scheduler instrumentation
4. **`scheduler/schedulerutils/buildworker.go`**: Worker instrumentation
5. **`go.mod`**: Added OpenTelemetry dependencies

### Key Functions

- `telemetry.Initialize()`: Sets up the OpenTelemetry provider
- `telemetry.StartSpan()`: Creates new spans
- `BuildRequestTelemetry()`: Adds attributes for build requests
- `BuildResultTelemetry()`: Adds attributes for build results

### Dependencies Added

```
go.opentelemetry.io/otel v1.28.0
go.opentelemetry.io/otel/exporters/otlp/otlptrace v1.28.0
go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc v1.28.0
go.opentelemetry.io/otel/sdk v1.28.0
go.opentelemetry.io/otel/trace v1.28.0
```

## Performance Considerations

- Telemetry has minimal overhead when disabled
- When enabled, spans are buffered and sent in batches
- No sensitive data is included in telemetry
- Graceful shutdown ensures all telemetry data is flushed

## Troubleshooting

### Common Issues

1. **"Failed to initialize telemetry"**: Check that the OTLP endpoint is reachable
2. **No traces appearing**: Verify the collector is running and accessible
3. **High overhead**: Consider adjusting sampling rates in the collector

### Debugging

Enable debug logging to see telemetry initialization:
```bash
./scheduler --log-level=debug [other args...]
```

## Future Enhancements

Potential improvements for the telemetry system:

1. **Metrics**: Add OpenTelemetry metrics for build durations, success rates, etc.
2. **Custom Samplers**: Implement intelligent sampling based on build type
3. **Resource Attributes**: Add more detailed resource information (hostname, version, etc.)
4. **Span Links**: Link related spans across different parts of the build process
5. **Baggage**: Pass context information through the entire build chain

## Security Considerations

- No sensitive information (secrets, credentials) is included in telemetry
- Package names and build information are considered non-sensitive
- Consider network security for telemetry endpoints in production environments

// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Package telemetry provides OpenTelemetry instrumentation for the toolkit.
package telemetry

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"os"
	"time"

	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/codes"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
	"go.opentelemetry.io/otel/trace"
)

const (
	// ServiceName is the name of the service for telemetry
	ServiceName = "azurelinux-toolkit"
	// ServiceVersion will be set from the toolkit version
	ServiceVersion = "unknown"
)

var (
	// GlobalTracer is the global tracer instance
	GlobalTracer trace.Tracer
	// isInitialized tracks whether telemetry has been initialized
	isInitialized bool
	// globalBuildID is the unique build ID for this execution
	globalBuildID string
)

// Config holds telemetry configuration
type Config struct {
	// ServiceName is the name of the service
	ServiceName string
	// ServiceVersion is the version of the service
	ServiceVersion string
	// OTLPEndpoint is the OTLP collector endpoint (defaults to OTEL_EXPORTER_OTLP_ENDPOINT env var)
	OTLPEndpoint string
	// Enabled controls whether telemetry is enabled
	Enabled bool
	// BuildID is the unique identifier for the build, generated at random
	BuildID string
}

// generateBuildID creates a new unique build identifier
func generateBuildID() string {
	// Generate 8 random bytes (16 hex characters)
	bytes := make([]byte, 8)
	if _, err := rand.Read(bytes); err != nil {
		// Fallback to timestamp-based ID if random generation fails
		return fmt.Sprintf("build-%d", time.Now().Unix())
	}
	return hex.EncodeToString(bytes)
}

// GetOrCreateBuildID returns the global build ID, creating one if it doesn't exist
func GetOrCreateBuildID() string {
	if globalBuildID == "" {
		globalBuildID = generateBuildID()
	}
	return globalBuildID
}

// DefaultConfig returns a default telemetry configuration
func DefaultConfig() *Config {
	return DefaultConfigWithBuildID("")
}

// DefaultConfigWithBuildID returns a default telemetry configuration with an optional build ID
func DefaultConfigWithBuildID(buildID string) *Config {
	endpoint := os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT")

	// Enable telemetry if OTLP endpoint is configured and SDK is not explicitly disabled
	enabled := endpoint != "" && os.Getenv("OTEL_SDK_DISABLED") != "true"

	// Use provided build ID or generate one if empty
	if buildID == "" {
		buildID = GetOrCreateBuildID()
	} else {
		// Store the provided build ID globally
		globalBuildID = buildID
	}

	return &Config{
		ServiceName:    ServiceName,
		ServiceVersion: ServiceVersion,
		OTLPEndpoint:   endpoint,
		Enabled:        enabled,
		BuildID:        buildID,
	}
}

// TracerProvider holds the tracer provider instance
type TracerProvider struct {
	provider *sdktrace.TracerProvider
}

// Initialize sets up OpenTelemetry with the given configuration
func Initialize(ctx context.Context, config *Config) (*TracerProvider, error) {
	if !config.Enabled {
		// Set up a no-op tracer if telemetry is disabled
		GlobalTracer = otel.Tracer(config.ServiceName)
		return &TracerProvider{}, nil
	}

	// Create resource with service information
	res, err := resource.New(ctx,
		resource.WithAttributes(
			semconv.ServiceName(config.ServiceName),
			semconv.ServiceVersion(config.ServiceVersion),
			attribute.String("build.id", config.BuildID),
		),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create resource: %w", err)
	}

	// Create OTLP exporter
	var exporter sdktrace.SpanExporter
	if config.OTLPEndpoint != "" {
		client := otlptracegrpc.NewClient(
			otlptracegrpc.WithEndpoint(config.OTLPEndpoint),
			otlptracegrpc.WithInsecure(), // Use insecure for local development, configure TLS for production
		)
		exporter, err = otlptrace.New(ctx, client)
		if err != nil {
			return nil, fmt.Errorf("failed to create OTLP exporter for endpoint %s: %w", config.OTLPEndpoint, err)
		}
	} else {
		// No endpoint configured, return error with helpful message
		return nil, fmt.Errorf("telemetry is enabled but no OTLP endpoint is configured. Set OTEL_EXPORTER_OTLP_ENDPOINT environment variable or use --otlp-endpoint flag")
	}

	// Create tracer provider
	tp := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(exporter),
		sdktrace.WithResource(res),
		sdktrace.WithSampler(sdktrace.AlwaysSample()),
	)

	// Set global tracer provider and propagator
	otel.SetTracerProvider(tp)
	otel.SetTextMapPropagator(propagation.TraceContext{})

	// Set global tracer
	GlobalTracer = otel.Tracer(config.ServiceName)

	// Store the build ID globally for cross-tool consistency
	globalBuildID = config.BuildID
	isInitialized = true

	return &TracerProvider{provider: tp}, nil
}

// Shutdown gracefully shuts down the tracer provider
func (tp *TracerProvider) Shutdown(ctx context.Context) error {
	if tp.provider != nil {
		return tp.provider.Shutdown(ctx)
	}
	return nil
}

// SetBuildID sets the global build ID
func SetBuildID(buildID string) {
	globalBuildID = buildID
}

// GetBuildID returns the current build ID
func GetBuildID() string {
	return globalBuildID
}

// StartSpan starts a new span with the given name and options
func StartSpan(ctx context.Context, spanName string, opts ...trace.SpanStartOption) (context.Context, trace.Span) {
	if !isInitialized || GlobalTracer == nil {
		// Return a no-op span if telemetry is not initialized
		return ctx, trace.SpanFromContext(ctx)
	}

	// Add build ID as a span attribute if available
	if globalBuildID != "" {
		opts = append(opts, trace.WithAttributes(attribute.String("build.id", globalBuildID)))
	}

	return GlobalTracer.Start(ctx, spanName, opts...)
}

// AddEvent adds an event to the span in the current context
func AddEvent(ctx context.Context, name string, attrs ...attribute.KeyValue) {
	span := trace.SpanFromContext(ctx)
	if span != nil {
		span.AddEvent(name, trace.WithAttributes(attrs...))
	}
}

// SetAttributes sets attributes on the span in the current context
func SetAttributes(ctx context.Context, attrs ...attribute.KeyValue) {
	span := trace.SpanFromContext(ctx)
	if span != nil {
		span.SetAttributes(attrs...)
	}
}

// RecordError records an error on the span in the current context
func RecordError(ctx context.Context, err error, attrs ...attribute.KeyValue) {
	span := trace.SpanFromContext(ctx)
	if span != nil {
		span.RecordError(err, trace.WithAttributes(attrs...))
	}
}

// SetStatus sets the status of the span in the current context
func SetStatus(ctx context.Context, code codes.Code, description string) {
	span := trace.SpanFromContext(ctx)
	if span != nil {
		span.SetStatus(code, description)
	}
}

// InstrumentedTimer creates a timer that automatically records duration as a span
type InstrumentedTimer struct {
	ctx       context.Context
	span      trace.Span
	startTime time.Time
}

// NewTimer creates a new instrumented timer
func NewTimer(ctx context.Context, spanName string, opts ...trace.SpanStartOption) *InstrumentedTimer {
	spanCtx, span := StartSpan(ctx, spanName, opts...)
	return &InstrumentedTimer{
		ctx:       spanCtx,
		span:      span,
		startTime: time.Now(),
	}
}

// Stop stops the timer and records the duration
func (t *InstrumentedTimer) Stop() time.Duration {
	duration := time.Since(t.startTime)
	if t.span != nil {
		t.span.SetAttributes(attribute.Int64("duration_ms", duration.Milliseconds()))
		t.span.End()
	}
	return duration
}

// Context returns the context with the span
func (t *InstrumentedTimer) Context() context.Context {
	return t.ctx
}

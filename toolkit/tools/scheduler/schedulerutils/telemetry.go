// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package schedulerutils

import (
	"context"
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/telemetry"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/codes"
	"go.opentelemetry.io/otel/trace"
)

// BuildRequestTelemetry adds telemetry attributes for a build request
func BuildRequestTelemetry(ctx context.Context, req *BuildRequest) context.Context {
	if req == nil || req.Node == nil {
		return ctx
	}

	telemetry.SetAttributes(ctx,
		attribute.String("package.name", req.Node.FriendlyName()),
		attribute.String("package.type", req.Node.Type.String()),
		attribute.String("package.architecture", req.Node.Architecture),
		attribute.String("package.source_name", req.Node.SrpmPath),
		attribute.Bool("package.use_cache", req.UseCache),
		attribute.Bool("package.is_delta", req.IsDelta),
		attribute.Int("package.freshness", int(req.Freshness)),
	)

	return ctx
}

// BuildResultTelemetry adds telemetry attributes for a build result
func BuildResultTelemetry(ctx context.Context, res *BuildResult) context.Context {
	if res == nil || res.Node == nil {
		return ctx
	}

	attrs := []attribute.KeyValue{
		attribute.String("package.name", res.Node.FriendlyName()),
		attribute.String("package.type", res.Node.Type.String()),
		attribute.Bool("build.success", res.Err == nil),
		attribute.Bool("build.was_delta", res.WasDelta),
		attribute.Bool("build.used_cache", res.UsedCache),
		attribute.Int("build.files_built_count", len(res.BuiltFiles)),
		attribute.Bool("build.ignored", res.Ignored),
		attribute.Bool("test.check_failed", res.CheckFailed),
		attribute.Int("package.freshness", int(res.Freshness)),
	}

	if res.Err != nil {
		attrs = append(attrs, attribute.String("build.error", res.Err.Error()))
		telemetry.RecordError(ctx, res.Err)
		telemetry.SetStatus(ctx, codes.Error, "Build failed")
	} else {
		telemetry.SetStatus(ctx, codes.Ok, "Build completed successfully")
	}

	// Add log file information if available
	if res.LogFile != "" {
		attrs = append(attrs, attribute.String("build.log_file", res.LogFile))
	}

	if res.HasLicenseWarnings {
		attrs = append(attrs, attribute.Bool("license.has_warnings", true))
	}

	if res.HasLicenseErrors {
		attrs = append(attrs, attribute.Bool("license.has_errors", true))
	}

	telemetry.SetAttributes(ctx, attrs...)
	return ctx
}

// WorkerTelemetry creates a span for a build worker
func WorkerTelemetry(ctx context.Context, workerID int) (context.Context, trace.Span) {
	return telemetry.StartSpan(ctx, "scheduler.worker",
		trace.WithAttributes(
			attribute.Int("worker.id", workerID),
		),
	)
}

// PackageBuildTelemetry creates a span for building a specific package
func PackageBuildTelemetry(ctx context.Context, req *BuildRequest) (context.Context, trace.Span) {
	if req == nil || req.Node == nil {
		return telemetry.StartSpan(ctx, "scheduler.build.unknown")
	}

	spanName := fmt.Sprintf("scheduler.build.%s", req.Node.Type.String())
	return telemetry.StartSpan(ctx, spanName,
		trace.WithAttributes(
			attribute.String("package.name", req.Node.FriendlyName()),
			attribute.String("package.type", req.Node.Type.String()),
			attribute.String("package.architecture", req.Node.Architecture),
			attribute.Bool("package.use_cache", req.UseCache),
			attribute.Bool("package.is_delta", req.IsDelta),
			attribute.Int("package.freshness", int(req.Freshness)),
		),
	)
}

// GraphBuildTelemetry creates a span for the overall graph build process
func GraphBuildTelemetry(ctx context.Context, nodeCount, workerCount int) (context.Context, trace.Span) {
	return telemetry.StartSpan(ctx, "scheduler.build_graph",
		trace.WithAttributes(
			attribute.Int("graph.node_count", nodeCount),
			attribute.Int("scheduler.worker_count", workerCount),
		),
	)
}

// LicenseCheckTelemetry creates a span for license checking
func LicenseCheckTelemetry(ctx context.Context, packageName string) (context.Context, trace.Span) {
	return telemetry.StartSpan(ctx, "scheduler.license_check",
		trace.WithAttributes(
			attribute.String("package.name", packageName),
		),
	)
}

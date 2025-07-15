// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A very simple replacement for wget.

package main

import (
	"context"
	"crypto/tls"
	"crypto/x509"
	"net/url"
	"os"
	"path/filepath"
	"time"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/network"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/telemetry"
	"github.com/sirupsen/logrus"

	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/codes"
	"go.opentelemetry.io/otel/trace"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("downloader", "Download files to a location")

	logFlags  = exe.SetupLogFlags(app)
	noClobber = app.Flag("no-clobber", "Do not overwrite existing files").Bool()
	noVerbose = app.Flag("no-verbose", "Do not print verbose output").Bool()

	caCertFile    = app.Flag("ca-certificate", "Root certificate authority to use when downloading files.").String()
	tlsClientCert = app.Flag("certificate", "TLS client certificate to use when downloading files.").String()
	tlsClientKey  = app.Flag("private-key", "TLS client key to use when downloading files.").String()

	dstFile   = app.Flag("output-file", "Destination file to download to").Short('O').String()
	prefixDir = app.Flag("directory-prefix", "Directory to download to").Short('P').String()
	srcUrl    = app.Arg("url", "URL to download").Required().String()

	// Telemetry flags
	enableTelemetry = app.Flag("enable-telemetry", "Enable OpenTelemetry tracing.").Bool()
	otlpEndpoint    = app.Flag("otlp-endpoint", "OTLP collector endpoint for telemetry export.").Default("").String()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)
	if *noVerbose {
		logger.Log.SetLevel(logrus.WarnLevel)
	}

	// Initialize telemetry
	ctx := context.Background()
	telemetryConfig := telemetry.DefaultConfig()
	telemetryConfig.ServiceName = "azurelinux-toolkit-downloader"
	telemetryConfig.ServiceVersion = exe.ToolkitVersion

	// Override with command line flags if provided
	if *enableTelemetry {
		telemetryConfig.Enabled = true
	}
	if *otlpEndpoint != "" {
		telemetryConfig.OTLPEndpoint = *otlpEndpoint
		telemetryConfig.Enabled = true
	}

	var tracerProvider *telemetry.TracerProvider
	if telemetryConfig.Enabled {
		var err error
		tracerProvider, err = telemetry.Initialize(ctx, telemetryConfig)
		if err != nil {
			logger.Log.Warnf("Failed to initialize telemetry: %s", err)
		} else {
			logger.Log.Infof("Telemetry initialized with endpoint: %s", telemetryConfig.OTLPEndpoint)
			defer func() {
				shutdownCtx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
				defer cancel()
				if err := tracerProvider.Shutdown(shutdownCtx); err != nil {
					logger.Log.Warnf("Failed to shutdown telemetry: %s", err)
				}
			}()
		}
	}

	// Create main span for the entire downloader run
	ctx, mainSpan := telemetry.StartSpan(ctx, "downloader.main",
		trace.WithAttributes(
			attribute.String("downloader.version", exe.ToolkitVersion),
			attribute.String("downloader.source_url", *srcUrl),
		),
	)
	defer mainSpan.End()

	caCerts, err := x509.SystemCertPool()
	if err != nil {
		logger.Log.Fatalf("Failed to load system certificate pool. Error:\n%s", err)
	}
	if *caCertFile != "" {
		newCACert, err := os.ReadFile(*caCertFile)
		if err != nil {
			logger.Log.Fatalf("Invalid CA certificate (%s), Error:\n%s", *caCertFile, err)
		}

		caCerts.AppendCertsFromPEM(newCACert)
	}

	var tlsCerts []tls.Certificate
	if *tlsClientCert != "" && *tlsClientKey != "" {
		cert, err := tls.LoadX509KeyPair(*tlsClientCert, *tlsClientKey)
		if err != nil {
			logger.Log.Fatalf("Invalid TLS client key pair (%s) (%s), Error:\n%s", *tlsClientCert, *tlsClientKey, err)
		}

		tlsCerts = append(tlsCerts, cert)
	}

	// dst may be empty, in which case the file will be downloaded to the current directory. Generate dst from src's basename.
	// The url may include query strings which should be stripped.
	if *dstFile != "" && *prefixDir != "" {
		logger.Log.Fatalf("Cannot specify both --output-file and --directory-prefix")
	}
	if *dstFile == "" {
		// strip query strings from url
		u, err := url.Parse(*srcUrl)
		if err != nil {
			logger.Log.Fatalf("Invalid URL (%s), Error:\n%s", *srcUrl, err)
		}
		*dstFile = filepath.Base(u.Path)
		if *prefixDir != "" {
			*dstFile = filepath.Join(*prefixDir, *dstFile)
		}
	}

	if *noClobber {
		exists, err := file.PathExists(*dstFile)
		if err != nil {
			logger.Log.Fatalf("Failed to check if file (%s) exists. Error:\n%s", *dstFile, err)
		}
		if exists {
			logger.Log.Infof("File (%s) already exists, skipping download", *dstFile)
			return
		}
	}

	// Create span for the download operation
	downloadCtx, downloadSpan := telemetry.StartSpan(ctx, "downloader.download",
		trace.WithAttributes(
			attribute.String("download.url", *srcUrl),
			attribute.String("download.destination", *dstFile),
		),
	)
	defer downloadSpan.End()

	_, err = network.DownloadFileWithRetry(downloadCtx, *srcUrl, *dstFile, caCerts, tlsCerts, network.DefaultTimeout)
	if err != nil {
		telemetry.RecordError(downloadCtx, err)
		telemetry.SetStatus(downloadCtx, codes.Error, "Download failed")
		logger.Log.Fatalf("Failed to download (%s) to (%s). Error:\n%s", *srcUrl, *dstFile, err)
	}

	telemetry.SetStatus(downloadCtx, codes.Ok, "Download completed successfully")
	telemetry.AddEvent(downloadCtx, "download_completed",
		attribute.String("file_path", *dstFile),
	)
}

// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A very simple replacement for wget.

package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"net/url"
	"os"
	"path/filepath"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/exe"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/network"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/sirupsen/logrus"

	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	app = kingpin.New("downloader", "Download files to a location")

	logFile   = exe.LogFileFlag(app)
	logLevel  = exe.LogLevelFlag(app)
	noClobber = app.Flag("no-clobber", "Do not overwrite existing files").Bool()
	noVerbose = app.Flag("no-verbose", "Do not print verbose output").Bool()
	timeout   = app.Flag("timeout", "Stops retrying after this duration (up to the max of 6 attempts)").Default("0").Duration()

	caCertFile    = app.Flag("ca-certificate", "Root certificate authority to use when downloading files.").String()
	tlsClientCert = app.Flag("certificate", "TLS client certificate to use when downloading files.").String()
	tlsClientKey  = app.Flag("private-key", "TLS client key to use when downloading files.").String()

	dstFile   = app.Flag("output-file", "Destination file to download to").Short('O').String()
	prefixDir = app.Flag("directory-prefix", "Directory to download to").Short('P').String()
	srcUrl    = app.Arg("url", "URL to download").Required().String()
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(*logFile, *logLevel)
	if *noVerbose {
		logger.Log.SetLevel(logrus.WarnLevel)
	}

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
			logger.Log.Infof("File (%s) already exists, skipping download.", *dstFile)
			return
		}
	}

	err = downloadFile(*srcUrl, *dstFile, caCerts, tlsCerts, *timeout)
	if err != nil {
		logger.Log.Fatalf("Failed to download (%s) to (%s). Error:\n%s", *srcUrl, *dstFile, err)
	}
}

func downloadFile(srcUrl, dstFile string, caCerts *x509.CertPool, tlsCerts []tls.Certificate, timeout time.Duration) (err error) {
	const (
		// With 6 attempts, initial delay of 1 second, and a backoff factor of 3.0 the total time spent retrying will be
		// 1 + 3 + 9 + 27 + 81 = 121 seconds.
		downloadRetryAttempts = 6
		failureBackoffBase    = 3.0
		downloadRetryDuration = time.Second
	)
	cancel := make(chan struct{})
	if timeout > 0 {
		go func() {
			time.Sleep(timeout)
			close(cancel)
		}()
	}

	retryNum := 1
	timedOut, err := retry.RunWithExpBackoff(func() error {
		netErr := network.DownloadFile(srcUrl, dstFile, caCerts, tlsCerts)
		if netErr != nil {
			// Check if the error contains the string "invalid response: 404", we should print a warning in that case so the
			// sees it even if we are running with --no-verbose.
			if netErr.Error() == "invalid response: 404" {
				logger.Log.Warnf("Attempt %d/%d: Failed to download '%s' with error: '%s'", retryNum, downloadRetryAttempts, srcUrl, netErr)
			} else {
				logger.Log.Infof("Attempt %d/%d: Failed to download '%s' with error: '%s'", retryNum, downloadRetryAttempts, srcUrl, netErr)
			}
		}
		retryNum++
		return netErr
	}, downloadRetryAttempts, downloadRetryDuration, failureBackoffBase, cancel)

	if timedOut {
		err = fmt.Errorf("timed out downloading (%s) after %s", srcUrl, timeout)
		return
	}

	if err != nil {
		err = fmt.Errorf("failed to download (%s) to (%s). Error:\n%w", srcUrl, dstFile, err)
	}
	return
}

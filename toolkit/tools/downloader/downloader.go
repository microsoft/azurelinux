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

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/network"
	"github.com/sirupsen/logrus"

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
)

func main() {
	app.Version(exe.ToolkitVersion)
	kingpin.MustParse(app.Parse(os.Args[1:]))
	logger.InitBestEffort(logFlags)
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
			logger.Log.Infof("File (%s) already exists, skipping download", *dstFile)
			return
		}
	}

	_, err = network.DownloadFileWithRetry(context.Background(), *srcUrl, *dstFile, caCerts, tlsCerts, network.DefaultTimeout)
	if err != nil {
		logger.Log.Fatalf("Failed to download (%s) to (%s). Error:\n%s", *srcUrl, *dstFile, err)
	}
}

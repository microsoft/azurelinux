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

	"github.com/microsoft/azurelinux/toolkit/tools/internal/exe"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/network"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/retry"
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

	dstFile     = app.Flag("output-file", "Destination file to download to").Short('O').String()
	prefixDir   = app.Flag("directory-prefix", "Directory to download to").Short('P').String()
	rpmFilename = app.Arg("rpm-filename", "RPM to download").Required().String()
	srcUrls     = app.Arg("url-list", "URLs to download").Required().Strings()
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

	for idx, srcUrl := range *srcUrls {
		localDstFile := *dstFile
		srcUrl = srcUrl + "/" + *rpmFilename
		if localDstFile == "" {
			// strip query strings from url
			_, err := url.Parse(srcUrl)
			if err != nil {
				// if the url is invalid, we need to log the error and continue to the next url
				// if the url is the last in the slice, which means we are unable to download the package
				// from all the previous urls, we should return an error
				if idx == len(*srcUrls)-1 {
					logger.Log.Fatalf("Invalid URL (%s), Error:\n%s", srcUrl, err)
				} else {
					logger.Log.Errorf("Invalid URL (%s), Error:\n%s", srcUrl, err)
					continue
				}
			}
			localDstFile = *rpmFilename
			if *prefixDir != "" {
				localDstFile = filepath.Join(*prefixDir, localDstFile)
			}
		}
		err = downloadFile(srcUrl, localDstFile, caCerts, tlsCerts)
		if err != nil {
			if idx == len(*srcUrls)-1 {
				logger.Log.Fatalf("Failed to download (%s) to (%s). Error:\n%s", srcUrl, localDstFile, err)
			} else {
				logger.Log.Errorf("Failed to download (%s) to (%s). Error:\n%s", srcUrl, localDstFile, err)
			}
		} else {
			break
		}
	}
}

func downloadFile(srcUrl, dstFile string, caCerts *x509.CertPool, tlsCerts []tls.Certificate) (err error) {
	cancel := make(chan struct{})
	retryNum := 1
	_, err = retry.RunWithDefaultDownloadBackoff(func() error {
		netErr := network.DownloadFile(srcUrl, dstFile, caCerts, tlsCerts)
		if netErr != nil {
			// Check if the error contains the string "invalid response: 404", we should print a warning in that case so the
			// sees it even if we are running with --no-verbose. 404's are unlikely to fix themselves on retry, give up.
			if netErr.Error() == "invalid response: 404" {
				logger.Log.Warnf("Attempt %d/%d: Failed to download '%s' with error: '%s'", retryNum, retry.DefaultDownloadRetryAttempts, srcUrl, netErr)
				logger.Log.Warnf("404 errors are likely unrecoverable, will not retry")
				close(cancel)
			} else {
				logger.Log.Infof("Attempt %d/%d: Failed to download '%s' with error: '%s'", retryNum, retry.DefaultDownloadRetryAttempts, srcUrl, netErr)
			}
		}
		retryNum++
		return netErr
	}, cancel)

	if err != nil {
		err = fmt.Errorf("failed to download (%s) to (%s). Error:\n%w", srcUrl, dstFile, err)
	}
	return
}

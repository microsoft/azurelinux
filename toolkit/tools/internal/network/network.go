// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package network

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

// JoinURL concatenates baseURL with extraPaths
func JoinURL(baseURL string, extraPaths ...string) string {
	const urlPathSeparator = "/"

	if len(extraPaths) == 0 {
		return baseURL
	}

	appendToBase := strings.Join(extraPaths, urlPathSeparator)
	return fmt.Sprintf("%s%s%s", baseURL, urlPathSeparator, appendToBase)
}

// DownloadFile downloads `url` into `dst`. `caCerts` may be nil.
func DownloadFile(url, dst string, caCerts *x509.CertPool, tlsCerts []tls.Certificate) (err error) {
	logger.Log.Debugf("Downloading (%s) -> (%s)", url, dst)

	dstFile, err := os.Create(dst)
	if err != nil {
		return
	}
	defer dstFile.Close()

	tlsConfig := &tls.Config{
		RootCAs:      caCerts,
		Certificates: tlsCerts,
	}
	transport := http.DefaultTransport.(*http.Transport).Clone()
	transport.TLSClientConfig = tlsConfig
	client := &http.Client{
		Transport: transport,
	}

	response, err := client.Get(url)
	if err != nil {
		return
	}
	defer response.Body.Close()

	if response.StatusCode != http.StatusOK {
		return fmt.Errorf("invalid response: %v", response.StatusCode)
	}

	_, err = io.Copy(dstFile, response.Body)

	return
}

// CheckNetworkAccess checks whether the installer environment has network access
func CheckNetworkAccess() (err error, hasNetworkAccess bool) {
	const (
		retryAttempts = 10
		retryDuration = time.Second
		squashErrors  = false
	)

	err = retry.Run(func() error {
		err := shell.ExecuteLive(squashErrors, "ping", "-c", "1", "www.microsoft.com")
		hasNetworkAccess = err == nil
		if !hasNetworkAccess {
			logger.Log.Warnf("No network access yet")
		}

		return err
	}, retryAttempts, retryDuration)

	if err != nil {
		logger.Log.Errorf("Failure in multiple attempts to check network access")
	}

	return
}

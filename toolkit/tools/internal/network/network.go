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

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/retry"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
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

// DownloadFile downloads `url` into `dst`. `caCerts` may be nil. If there is an error `dst` will be removed.
func DownloadFile(url, dst string, caCerts *x509.CertPool, tlsCerts []tls.Certificate) (err error) {
	logger.Log.Debugf("Downloading (%s) -> (%s)", url, dst)

	dstFile, err := os.Create(dst)
	if err != nil {
		return
	}
	defer func() {
		// If there was an error, ensure that the file is removed
		if err != nil {
			cleanupErr := file.RemoveFileIfExists(dst)
			if cleanupErr != nil {
				logger.Log.Errorf("Failed to remove failed network download file '%s': %s", dst, err)
			}
		}
		dstFile.Close()
	}()

	tlsConfig := &tls.Config{
		RootCAs:      caCerts,
		Certificates: tlsCerts,
	}
	transport := http.DefaultTransport.(*http.Transport).Clone()
	transport.TLSClientConfig = tlsConfig
	// Default is 10 seconds, we increase to 30 seconds to mitigate TLS handshake timeout errors
	// we're seeing from some upstream RPM package sources
	transport.TLSHandshakeTimeout = 30 * time.Second
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
// This function is only executed within the ISO installation environment for kickstart-like unattended installation
func CheckNetworkAccess() (err error, hasNetworkAccess bool) {
	const (
		retryAttempts = 10
		retryDuration = time.Second
		squashErrors  = false
		activeStatus  = "active"
	)

	err = retry.Run(func() error {
		err := shell.ExecuteLive(squashErrors, "systemctl", "restart", "systemd-networkd-wait-online")
		if err != nil {
			logger.Log.Errorf("Cannot start systemd-networkd-wait-online.service")
			return err
		}

		stdout, stderr, err := shell.Execute("systemctl", "is-active", "systemd-networkd-wait-online")
		if err != nil {
			logger.Log.Errorf("Failed to query status of systemd-networkd-wait-online: %v", stderr)
			return err
		}

		serviceStatus := strings.TrimSpace(stdout)
		hasNetworkAccess = serviceStatus == activeStatus
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

// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package network

import (
	"context"
	"crypto/tls"
	"crypto/x509"
	"errors"
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

// ErrDownloadFileInvalidResponse404 is returned when the download response is 404.
var ErrDownloadFileInvalidResponse404 = errors.New("invalid response: 404")

// ErrDownloadFileOther is returned when the download error is anything other than 404.
var ErrDownloadFileOther = errors.New("download error")

func buildResponseError(statusCode int) error {
	if statusCode == http.StatusNotFound {
		return ErrDownloadFileInvalidResponse404
	} else {
		return fmt.Errorf("%w: %d", ErrDownloadFileOther, statusCode)
	}
}

// JoinURL concatenates baseURL with extraPaths
func JoinURL(baseURL string, extraPaths ...string) string {
	const urlPathSeparator = "/"

	if len(extraPaths) == 0 {
		return baseURL
	}

	appendToBase := strings.Join(extraPaths, urlPathSeparator)
	return fmt.Sprintf("%s%s%s", baseURL, urlPathSeparator, appendToBase)
}

// DownloadFile downloads a file from a URL to a local file. It will retry the download if it fails. If the externalCancel
// channel is provided, the download will be cancelled if the externalCancel channel is closed. The function will return
// true if the download was cancelled, and an error if the download failed. 404 errors are considered unrecoverable and
// will not be retried.
// srcUrl: The URL to download from.
// dstFile: The local file to save the download to.
// caCerts: The CA certificates to use for the download.
// tlsCerts: The TLS certificates to use for the download.
// externalCancel: An optional channel that can be used to cancel the download, pass nil if not needed.
// returns: wasCancelled: true if the download was cancelled via the external cancel channel, false otherwise.
// returns: err: An error if the download failed (including being cancelled), nil otherwise.
func DownloadFileWithRetry(ctx context.Context, srcUrl, dstFile string, caCerts *x509.CertPool, tlsCerts []tls.Certificate) (wasCancelled bool, err error) {
	if ctx == nil {
		return false, fmt.Errorf("context is nil")
	}
	retryCtx, cancelFunc := context.WithCancel(ctx)
	defer cancelFunc()

	retryNum := 1
	errorWas404 := false
	wasCancelled, err = retry.RunWithDefaultDownloadBackoff(retryCtx, func() error {
		netErr := DownloadFile(srcUrl, dstFile, caCerts, tlsCerts)
		if netErr != nil {
			// Check if the error contains the string "invalid response: 404", we should print a warning in that case so the
			// sees it even if we are running with --no-verbose. 404's are unlikely to fix themselves on retry, give up.
			if errors.Is(netErr, ErrDownloadFileInvalidResponse404) {
				logger.Log.Warnf("Attempt %d/%d: Failed to download (%s) with error: (%s)", retryNum, retry.DefaultDownloadRetryAttempts, srcUrl, netErr)
				logger.Log.Warnf("404 errors are likely unrecoverable, will not retry")
				errorWas404 = true
				cancelFunc()
			} else {
				logger.Log.Infof("Attempt %d/%d: Failed to download (%s) with error: (%s)", retryNum, retry.DefaultDownloadRetryAttempts, srcUrl, netErr)
			}
		}
		retryNum++
		return netErr
	})

	// If the error was a 404, we should not consider the download as cancelled
	if errorWas404 {
		wasCancelled = false
	}

	if err != nil {
		err = fmt.Errorf("failed to download (%s) to (%s):\n%w", srcUrl, dstFile, err)
	}
	return
}

// DownloadFile downloads `url` into `dst`. `caCerts` may be nil. If there is an error `dst` will be removed.
func DownloadFile(url, dst string, caCerts *x509.CertPool, tlsCerts []tls.Certificate) (err error) {
	logger.Log.Debugf("Downloading (%s) -> (%s)", url, dst)

	dstFile, err := os.Create(dst)
	if err != nil {
		return fmt.Errorf("%w:\nfailed to create file:\n%w", ErrDownloadFileOther, err)
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
	client := &http.Client{
		Transport: transport,
	}

	response, err := client.Get(url)
	if err != nil {
		return fmt.Errorf("%w:\nrequest failed:\n%w", ErrDownloadFileOther, err)
	}
	defer response.Body.Close()

	if response.StatusCode != http.StatusOK {
		return buildResponseError(response.StatusCode)
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

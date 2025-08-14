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

	"github.com/microsoft/azurelinux/toolkit/tools/internal/azureblobstorage"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/retry"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

const (
	// Default upper bound on a single network operation, across all retries.
	DefaultTimeout = time.Minute * 20
)

// ErrDownloadFileInvalidResponse404 is returned when the download response is 404.
var ErrDownloadFileInvalidResponse404 = errors.New("invalid response: 404")

// ErrDownloadFileInvalidTimeout is returned when the download timeout is invalid, i.e. less than 0.
var ErrDownloadFileInvalidTimeout = errors.New("invalid timeout")

// ErrDownloadFileOther is returned when the download error is anything other than 404.
var ErrDownloadFileOther = errors.New("download error")

// ErrDownloadFileSDKFallback is returned when both HTTP and Azure SDK downloads fail.
var ErrDownloadFileSDKFallback = errors.New("both HTTP and Azure SDK downloads failed.")

func buildResponseError(statusCode int) error {
	if statusCode == http.StatusNotFound {
		return ErrDownloadFileInvalidResponse404
	} else {
		return fmt.Errorf("%w: %d", ErrDownloadFileOther, statusCode)
	}
}

func buildResponseErrorSDKFallback(httpError error, azureError error) error {
	return fmt.Errorf("%w HTTP error: %w, Azure SDK error: %v", ErrDownloadFileSDKFallback, httpError, azureError)
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

// DownloadFileWithRetry downloads a file from a URL to a local file. It will retry the download if it fails. If the externalCancel
// channel is provided, the download will be cancelled if the externalCancel channel is closed. The function will return
// true if the download was cancelled, and an error if the download failed. 404 errors are considered unrecoverable and
// will not be retried.
// ctx: The context to use for the download. Use context.Background() if no other context is available.
// srcUrl: The URL to download from.
// dstFile: The local file to save the download to.
// caCerts: The CA certificates to use for the download.
// tlsCerts: The TLS certificates to use for the download.
// timeout: The maximum duration for the download operation, use 0 for no timeout, or network.DefaultTimeout for a default timeout.
// azureClientID: Optional Azure client ID for managed identity authentication.
// returns: wasCancelled: true if the download was cancelled via the external cancel channel, false otherwise.
// returns: err: An error if the download failed (including being cancelled), nil otherwise.
func DownloadFileWithRetry(
	ctx context.Context,
	srcUrl, dstFile string,
	caCerts *x509.CertPool,
	tlsCerts []tls.Certificate,
	azureClientID string,
	timeout time.Duration,
) (wasCancelled bool, err error) {
	var closeCtx context.CancelFunc

	if ctx == nil {
		return false, fmt.Errorf("context is nil")
	}

	if timeout < 0 {
		return false, fmt.Errorf("%w: %s", ErrDownloadFileInvalidTimeout, timeout)
	}

	if timeout == 0 {
		ctx, closeCtx = context.WithCancel(ctx)
	} else {
		ctx, closeCtx = context.WithTimeout(ctx, timeout)
	}
	defer closeCtx()

	retryNum := 1
	errorWas404 := false
	wasCancelled, err = retry.RunWithDefaultDownloadBackoff(ctx, func() error {
		netErr := DownloadFile(ctx, srcUrl, dstFile, caCerts, tlsCerts, azureClientID)
		if netErr != nil {
			// Check if the error is a 404, we should print a warning in that case so the user
			// sees it even if we are running with --no-verbose. 404's are unlikely to fix themselves on retry, give up.
			if errors.Is(netErr, ErrDownloadFileInvalidResponse404) {
				logger.Log.Warnf("Attempt %d/%d: Failed to download (%s) with error: (%s)", retryNum, retry.DefaultDownloadRetryAttempts, srcUrl, netErr)
				logger.Log.Warnf("404 errors are likely unrecoverable, will not retry")
				errorWas404 = true
				closeCtx()
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
// First attempts HTTP download, then falls back to Azure SDK if the URL is an Azure Blob Storage URL.
func DownloadFile(
	ctx context.Context,
	url, dst string,
	caCerts *x509.CertPool,
	tlsCerts []tls.Certificate,
	azureClientID string,
) (err error) {
	if ctx == nil {
		return fmt.Errorf("context is nil")
	}

	// First attempt HTTP download
	err = downloadFileHttp(ctx, url, dst, caCerts, tlsCerts)
	if err == nil {
		return nil // HTTP download succeeded
	}

	// HTTP download failed, attempt to parse as Azure Blob Storage URL
	blobInfo, parseErr := azureblobstorage.ParseAzureBlobStorageURL(url)
	if parseErr != nil {
		return buildResponseErrorSDKFallback(err, parseErr)
	}

	logger.Log.Debugf("HTTP download failed for Azure Blob Storage URL, attempting Azure SDK fallback")

	// Attempt download using Azure SDK
	azureErr := downloadFileWithAzureSDK(ctx, blobInfo, dst, azureClientID)
	if azureErr != nil {
		return buildResponseErrorSDKFallback(err, azureErr)
	}

	logger.Log.Infof("Azure SDK fallback succeeded for URL: %s", url)
	return nil
}

// downloadFileHttp attempts to download a file using HTTP with optional TLS configuration.
func downloadFileHttp(
	ctx context.Context,
	url, dst string,
	caCerts *x509.CertPool,
	tlsCerts []tls.Certificate,
) (err error) {
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
	// Default is 10 seconds, we increase to 30 seconds to mitigate TLS handshake timeout errors
	// we're seeing from some upstream RPM package sources
	transport.TLSHandshakeTimeout = 30 * time.Second
	client := &http.Client{
		Transport: transport,
	}

	request, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return fmt.Errorf("%w:\nfailed to create request:\n%w", ErrDownloadFileOther, err)
	}

	response, err := client.Do(request)
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

// downloadFileWithAzureSDK attempts to download a file from an Azure Blob Storage using the Azure SDK for Go
func downloadFileWithAzureSDK(
	ctx context.Context,
	blobInfo *azureblobstorage.AzureBlobInfo,
	dst string,
	azureClientID string,
) error {
	logger.Log.Infof("Attempting Azure SDK download for blob: %s/%s from storage account: %s",
		blobInfo.ContainerName, blobInfo.BlobName, blobInfo.StorageAccount)

	// Create Azure Blob Storage client with managed identity access
	azureBlobStorage, err := azureblobstorage.Create(
		"",
		"",
		"",
		blobInfo.StorageAccount,
		azureblobstorage.ManagedIdentityAccess,
		azureClientID)
	if err != nil {
		return fmt.Errorf("failed to create Azure Blob Storage client: %w", err)
	}

	// Attempt to download the blob
	err = azureBlobStorage.Download(ctx, blobInfo.ContainerName, blobInfo.BlobName, dst)
	if err != nil {
		return fmt.Errorf("Azure SDK download failed: %w", err)
	}

	logger.Log.Debugf("Successfully downloaded blob using Azure SDK")
	return nil
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

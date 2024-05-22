// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A very simple replacement for wget.

package downloader

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/network"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/retry"
)

func DownloadFile(srcUrl, dstFile string, caCerts *x509.CertPool, tlsCerts []tls.Certificate) (err error) {
	cancel := make(chan struct{})
	retryNum := 1
	_, err = retry.RunWithDefaultDownloadBackoff(func() error {
		netErr := network.DownloadFile(srcUrl, dstFile, caCerts, tlsCerts)
		if netErr != nil {
			// Check if the error contains the string "invalid response: 404", we should print a warning in that case so the
			// sees it even if we are running with --no-verbose. 404's are unlikely to fix themselves on retry, give up.
			if netErr.Error() == "invalid response: 404" {
				logger.Log.Warnf("Attempt %d/%d: Failed to download (%s) with error: (%s)", retryNum, retry.DefaultDownloadRetryAttempts, srcUrl, netErr)
				logger.Log.Warnf("404 errors are likely unrecoverable, will not retry")
				close(cancel)
			} else {
				logger.Log.Infof("Attempt %d/%d: Failed to download (%s) with error: (%s)", retryNum, retry.DefaultDownloadRetryAttempts, srcUrl, netErr)
			}
		}
		retryNum++
		return netErr
	}, cancel)

	if err != nil {
		err = fmt.Errorf("failed to download (%s) to (%s):\n%w", srcUrl, dstFile, err)
	}
	return
}

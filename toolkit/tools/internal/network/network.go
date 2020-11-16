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

	"microsoft.com/pkggen/internal/logger"
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
	transport := &http.Transport{
		TLSClientConfig: tlsConfig,
	}
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

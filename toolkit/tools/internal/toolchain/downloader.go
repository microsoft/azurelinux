// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package toolchain

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"io/fs"
	"os"
	"path/filepath"
	"sort"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/network"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/retry"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/sliceutils"
)

type downloadResultType int

const (
	downloadResultTypeSuccess downloadResultType = iota
	downloadResultTypeSkipped
	downloadResultTypeFailure404
	downloadResultTypeFailureOther
)

type downloadResult struct {
	toolchainRpm string
	result       downloadResultType
	err          error
}

// Remove any unepxected RPMs from the toolchain directory.
func CleanToolchainRpms(toolchainDir string, toolchainRPMs []string) (filesRemoved []string, err error) {
	exists, err := file.PathExists(toolchainDir)
	if err != nil {
		err = fmt.Errorf("failed to check if toolchain directory exists. Error:\n%w", err)
		return
	}
	if !exists {
		logger.Log.Debugf("Toolchain directory '%s' does not exist, skipping clean.", toolchainDir)
		return
	}

	expectedRpms := sliceutils.SliceToSet(toolchainRPMs)
	err = filepath.WalkDir(toolchainDir, func(path string, info fs.DirEntry, err error) error {
		if err != nil {
			return err
		}

		if info.IsDir() {
			return nil
		}

		if !expectedRpms[info.Name()] {
			logger.Log.Debugf("Removing unexpected file in toolchain directory: %s", path)
			filesRemoved = append(filesRemoved, path)
			return os.Remove(path)
		}

		return nil
	})

	if err != nil {
		logger.Log.Warnf("Unable to remove unexpected toolchain files: %s", err)
	}

	return
}

// downloadToolchainRpms checks for the existence of toolchain RPMs in the toolchain directory and downloads them if they are not present.
// It will check each package URL in order and download the first one that exists.
func DownloadToolchainRpms(toolchainDir string, toolchainRPMs []string, packageURLs []string, caCerts *x509.CertPool, tlsCerts []tls.Certificate, concurrentNetOps uint, manifestFile string) (downloadedRpms []string, err error) {
	// We will be downloading packages concurrently, so we need to keep track of when they are all done via a wait group. To
	// simplify the code just use goroutines with a semaphore channel to limit the number of concurrent network operations. Each
	// goroutine will handle a single package and will send the result of the download to a results channel. The main thread will
	// monitor the results channel and update the progress counter accordingly.
	netOpsSemaphore := make(chan struct{}, concurrentNetOps)
	results := make(chan downloadResult)

	for _, rpm := range toolchainRPMs {
		rpmPath := filepath.Join(toolchainDir, rpm)
		go downloadSingleToolchainRpm(packageURLs, rpm, rpmPath, caCerts, tlsCerts, netOpsSemaphore, results)
	}

	downloads, err := trackDownloadProgress(len(toolchainRPMs), results, len(toolchainRPMs), manifestFile)
	if err != nil {
		err = fmt.Errorf("failed to download toolchain RPMs. Error:\n%w", err)
		return
	}

	for _, rpm := range downloads {
		rpmPath := filepath.Join(toolchainDir, rpm)
		downloadedRpms = append(downloadedRpms, fmt.Sprintf("Downloaded: %s", rpmPath))
	}

	return
}

// downloadSingleToolchainRpm will download a file from a list of package URLs sources to a destination file. It will use the first
// source that returns correctly.
func downloadSingleToolchainRpm(packageURLs []string, rpmFile, dstFile string, caCerts *x509.CertPool, tlsCerts []tls.Certificate, netOpsSemaphore chan struct{}, results chan downloadResult) {
	var err error
	result := downloadResult{
		toolchainRpm: rpmFile,
		result:       downloadResultTypeFailureOther,
		err:          nil,
	}

	exists, rpmErr := file.PathExists(dstFile)
	if rpmErr == nil && exists {
		logger.Log.Debugf("Toolchain RPM '%s' already exists, skipping download.", dstFile)
		result.result = downloadResultTypeSkipped
		results <- result
		return
	}

	err, wasError404 := downloadFromMultipleBaseUrls(packageURLs, rpmFile, dstFile, caCerts, tlsCerts, netOpsSemaphore)

	result.err = err
	if wasError404 {
		result.result = downloadResultTypeFailure404
	} else if err != nil {
		result.result = downloadResultTypeFailureOther
	} else {
		result.result = downloadResultTypeSuccess
	}

	results <- result
}

func downloadFromMultipleBaseUrls(packageURLs []string, rpmFile, dstFile string, caCerts *x509.CertPool, tlsCerts []tls.Certificate, netOpsSemaphore chan struct{}) (err error, wasError404 bool) {
	const (
		// With 6 attempts, initial delay of 1 second, and a backoff factor of 3.0 the total time spent retrying will be
		// 1 + 3 + 9 + 27 + 81 = 121 seconds.
		downloadRetryAttempts = 6
		failureBackoffBase    = 3.0
		downloadRetryDuration = time.Second
		error404              = "invalid response: 404"
	)
	// Limit the number of concurrent network operations to avoid overloading the network. All work past this point
	// is either network related, or trivial, so we can safely hold the semaphore until we are done.
	netOpsSemaphore <- struct{}{}
	defer func() {
		<-netOpsSemaphore
	}()

	wasError404 = false
	// For each source, try to download the file.
	for _, url := range packageURLs {
		wasError404 = false
		rpmURL := fmt.Sprintf("%s/%s", url, rpmFile)
		logger.Log.Debugf("Downloading toolchain RPM %s from %s", rpmFile, rpmURL)

		retryNum := 1
		cancel := make(chan struct{})
		_, err = retry.RunWithExpBackoff(func() error {
			netErr := network.DownloadFile(rpmURL, dstFile, caCerts, tlsCerts)
			if netErr != nil {
				// Check if the error contains the string "invalid response: 404", we should print a warning in that case so the
				// sees it even if we are running with --no-verbose. 404's are unlikely to fix themselves on retry, give up.
				if netErr.Error() == error404 {
					logger.Log.Debugf("Attempt %d/%d: Failed to download '%s' with error: '%s'", retryNum, downloadRetryAttempts, rpmURL, netErr)
					logger.Log.Debugf("404 errors are likely unrecoverable, will not retry")
					close(cancel)
					wasError404 = true
				} else {
					logger.Log.Debugf("Attempt %d/%d: Failed to download '%s' with error: '%s'", retryNum, downloadRetryAttempts, rpmURL, netErr)
				}
			}
			retryNum++
			return netErr
		}, downloadRetryAttempts, downloadRetryDuration, failureBackoffBase, cancel)

		if err != nil {
			err = fmt.Errorf("failed to download (%s) to (%s). Error:\n%w", rpmURL, dstFile, err)
			// Continue trying, we will only preserve the last error since we don't know which URL will succeed.
		} else {
			// Download succeeded, we are done.
			break
		}
	}
	return
}

// trackDownloadProgress will monitor the results channel and update the progress counter accordingly while collecting errors.
func trackDownloadProgress(numExpectedResults int, results chan downloadResult, totalRPMs int, manifestFile string) (downloaded []string, err error) {
	// Collect the failures so we can print them at the end.
	var failuresOther, failures404, skipped []string

	for i := 0; i < numExpectedResults; i++ {
		progressString := fmt.Sprintf("%3d%%", ((i+1)*100)/totalRPMs)
		result := <-results
		switch result.result {
		case downloadResultTypeSuccess:
			logger.Log.Infof("%s: Successfully downloaded: '%s'", progressString, result.toolchainRpm)
			downloaded = append(downloaded, result.toolchainRpm)
		case downloadResultTypeFailure404:
			logger.Log.Infof("%s: Unavailable upstream: '%s'", progressString, result.toolchainRpm)
			failures404 = append(failures404, result.toolchainRpm)
		case downloadResultTypeFailureOther:
			logger.Log.Errorf("%s: Failed to download: '%s' with error: %s", progressString, result.toolchainRpm, result.err)
			failuresOther = append(failuresOther, result.toolchainRpm)
		case downloadResultTypeSkipped:
			logger.Log.Debugf("%s: Skipped download: '%s'", progressString, result.toolchainRpm)
			skipped = append(skipped, result.toolchainRpm)
		}
	}

	if len(downloaded) > 0 {
		logger.Log.Infof("Downloaded %d/%d toolchain RPMs", len(downloaded), totalRPMs)
	}
	if len(skipped) > 0 {
		logger.Log.Infof("Skipped %d/%d pre-downloaded toolchain RPMs", len(skipped), totalRPMs)
	}
	if len(failures404) > 0 {
		logger.Log.Infof("Unable to find %d/%d toolchain RPMs", len(failures404), totalRPMs)
	}
	if len(failuresOther) > 0 {
		logger.Log.Errorf("Failed to download %d/%d toolchain RPMs", len(failuresOther), totalRPMs)
		err = fmt.Errorf("failed to download %d/%d toolchain RPMs", len(failuresOther), totalRPMs)
		return
	}

	sort.Strings(downloaded)
	err = file.WriteLines(downloaded, manifestFile)
	if err != nil {
		err = fmt.Errorf("failed to write manifest file:\n%w", err)
		return
	}

	return
}

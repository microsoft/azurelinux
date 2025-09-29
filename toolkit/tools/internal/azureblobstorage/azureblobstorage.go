// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package azureblobstorage

import (
	"context"
	"errors"
	"fmt"
	"net/url"
	"os"
	"regexp"
	"strings"
	"time"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/Azure/azure-sdk-for-go/sdk/storage/azblob"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/retry"
)

const (
	AnonymousAccess        = 0
	ServicePrincipalAccess = 1
	AzureCLIAccess         = 2
)

// Azure SDK error for 404-like condition for storage blobs (a similar message is returned for storage containers):
// RESPONSE 404: 404 The specified blob does not exist.
// ERROR CODE: BlobNotFound
const AzureSDK404ErrorPattern = "RESPONSE 404"

var (
	// Every valid blob URL will be of the form: <storage_account>.blob.core.windows.net/<container>/<blob_name>
	// With <blob_name> being optional.
	//
	// For:
	//     https://mystorageaccount.blob.core.windows.net/mycontainer/my/blob/name
	//
	// We'd get:
	//   - storage account:	mystorageaccount
	//   - container:       mycontainer
	//   - blob name:       my/blob/name
	blobStorageURLRegex = regexp.MustCompile(`^([^.]+)\.blob\.core\.windows\.net/([^/]+)(?:/([^?#]+))?`)
)

const (
	blobStorageURLMatchSubString = iota
	blobStorageURLStorageName
	blobStorageURLContainerName
	blobStorageURLBlobName
	blobStorageURLMaxMatchLen
)

// ParseAzureBlobStorageURL parses an Azure Blob Storage URL and extracts storage account, container, and optionally blob information.
func ParseAzureBlobStorageURL(urlStr string) (storageAccountName, containerName, blobName string, err error) {
	parsedURL, err := url.Parse(urlStr)
	if err != nil {
		return "", "", "", fmt.Errorf("failed to parse URL (%s):\n%w", urlStr, err)
	}

	if parsedURL.Scheme == "" {
		return "", "", "", fmt.Errorf("URL (%s) is not a valid Azure Blob Storage URL - must start with a scheme", urlStr)
	}

	matches := blobStorageURLRegex.FindStringSubmatch(parsedURL.Host + parsedURL.Path)
	if len(matches) < blobStorageURLBlobName {
		return "", "", "", fmt.Errorf("URL (%s) is not a valid Azure Blob Storage URL"+
			" (expected: <scheme>://<storage_account>.blob.core.windows.net/<container>/<optional_blob_name>)", urlStr)
	}

	storageAccountName = matches[blobStorageURLStorageName]
	containerName = matches[blobStorageURLContainerName]

	if len(matches) > blobStorageURLBlobName {
		blobName = matches[blobStorageURLBlobName]
	}

	return storageAccountName, containerName, blobName, nil
}

type AzureBlobStorage struct {
	theClient *azblob.Client
}

func (abs *AzureBlobStorage) Upload(
	ctx context.Context,
	localFileName string,
	containerName string,
	blobName string) (err error) {

	uploadStartTime := time.Now()

	localFile, err := os.OpenFile(localFileName, os.O_RDONLY, 0)
	if err != nil {
		return fmt.Errorf("failed to open local file for upload:\n%w", err)
	}
	defer localFile.Close()

	_, err = abs.theClient.UploadFile(ctx, containerName, blobName, localFile, nil)
	if err != nil {
		return fmt.Errorf("failed to upload local file to blob:\n%w", err)
	}

	uploadEndTime := time.Now()
	logger.Log.Infof("  upload time: %s", uploadEndTime.Sub(uploadStartTime))

	return nil
}

func (abs *AzureBlobStorage) Download(
	ctx context.Context,
	containerName string,
	blobName string,
	localFileName string) (err error) {
	if ctx == nil {
		return fmt.Errorf("context is nil")
	}

	downloadStartTime := time.Now()

	localFile, err := os.Create(localFileName)
	if err != nil {
		return fmt.Errorf("  failed to create local file for download:\n%w", err)
	}

	defer func() {
		localFile.Close()
		// If there was an error, ensure that the file is removed
		if err != nil {
			cleanupErr := file.RemoveFileIfExists(localFileName)
			if cleanupErr != nil {
				logger.Log.Warnf("Failed to remove failed network download file '%s': %v", localFileName, err)
			}
		}
	}()

	_, err = abs.theClient.DownloadFile(ctx, containerName, blobName, localFile, nil)
	if err != nil {
		return fmt.Errorf("failed to download blob to local file:\n%w", err)
	}

	downloadEndTime := time.Now()
	logger.Log.Infof("  download time: %v", downloadEndTime.Sub(downloadStartTime))

	return nil
}

func (abs *AzureBlobStorage) Delete(
	ctx context.Context,
	containerName string,
	blobName string) (err error) {

	deleteStartTime := time.Now()
	_, err = abs.theClient.DeleteBlob(ctx, containerName, blobName, nil)
	if err != nil {
		return fmt.Errorf("failed to delete blob:\n%w", err)
	}
	deleteEndTime := time.Now()
	logger.Log.Infof("  delete time: %v", deleteEndTime.Sub(deleteStartTime))

	return nil
}

func Create(tenantId string, userName string, password string, storageAccount string, authenticationType int) (abs *AzureBlobStorage, err error) {
	url := "https://" + storageAccount + ".blob.core.windows.net/"

	abs = &AzureBlobStorage{}

	switch authenticationType {
	case AnonymousAccess:
		abs.theClient, err = azblob.NewClientWithNoCredential(url, nil)
		if err != nil {
			return nil, fmt.Errorf("unable to init azure blob storage read-only client:\n%w", err)
		}

		return abs, nil

	case ServicePrincipalAccess:
		credential, err := azidentity.NewClientSecretCredential(tenantId, userName, password, nil)
		if err != nil {
			return nil, fmt.Errorf("unable to init azure service principal identity:\n%w", err)
		}

		abs.theClient, err = azblob.NewClient(url, credential, nil)
		if err != nil {
			return nil, fmt.Errorf("unable to init azure blob storage read-write client:\n%w", err)
		}

		return abs, nil

	case AzureCLIAccess:
		credential, err := azidentity.NewAzureCLICredential(nil)
		if err != nil {
			return nil, fmt.Errorf("unable to init azure managed identity:\n%w", err)
		}

		abs.theClient, err = azblob.NewClient(url, credential, nil)
		if err != nil {
			return nil, fmt.Errorf("unable to init azure blob storage read-write client:\n%w", err)
		}

		return abs, nil
	}

	return nil, errors.New("unknown authentication type")
}

// CreateFromURL creates an AzureBlobStorage client from a storage account URL
func CreateFromURL(storageAccountURL string) (abs *AzureBlobStorage, err error) {
	// Parse the URL to extract storage account information
	storageAccountName, _, _, parseErr := ParseAzureBlobStorageURL(storageAccountURL)
	if parseErr != nil {
		return nil, fmt.Errorf("failed to parse storage account URL:\n%w", parseErr)
	}

	abs, err = Create("", "", "", storageAccountName, AzureCLIAccess)
	if err != nil {
		return nil, fmt.Errorf("failed to create Azure Blob Storage client:\n%w", err)
	}

	return abs, nil
}

// DownloadFileWithRetry downloads a file from an Azure Blob Storage using the Azure SDK for Go with retry logic
// ctx: The context to use for the download. Use context.Background() if no other context is available.
// azureBlobStorage: The Azure Blob Storage client.
// srcUrl: The full Azure Blob Storage URL including container and blob path.
// dstFile: The local file to save the download to.
// timeout: The maximum duration for the download operation, use 0 for no timeout.
// returns: wasCancelled: true if the download was cancelled via the context, false otherwise.
// returns: err: An error if the download failed (including being cancelled), nil otherwise.
func DownloadFileWithRetry(
	ctx context.Context,
	azureBlobStorage *AzureBlobStorage,
	srcUrl, dstFile string,
	timeout time.Duration,
) (wasCancelled bool, err error) {
	var closeCtx context.CancelFunc

	if ctx == nil {
		return false, fmt.Errorf("context is nil")
	}

	if timeout < 0 {
		return false, fmt.Errorf("invalid timeout: %s", timeout)
	}

	if timeout == 0 {
		ctx, closeCtx = context.WithCancel(ctx)
	} else {
		ctx, closeCtx = context.WithTimeout(ctx, timeout)
	}
	defer closeCtx()

	// Parse the URL to get container and blob names
	_, containerName, blobName, parseErr := ParseAzureBlobStorageURL(srcUrl)
	if parseErr != nil {
		return false, fmt.Errorf("failed to parse source URL:\n%w", parseErr)
	}

	logger.Log.Infof("Attempting Azure SDK download for blob (%s/%s)", containerName, blobName)

	retryNum := 1
	errorWas404 := false
	wasCancelled, err = retry.RunWithDefaultDownloadBackoff(ctx, func() error {
		netErr := azureBlobStorage.Download(ctx, containerName, blobName, dstFile)
		if netErr != nil {
			// Check if the error is a 404-like condition (blob or container not found)
			if strings.Contains(netErr.Error(), AzureSDK404ErrorPattern) {
				logger.Log.Warnf("Attempt %d/%d: failed to download (%s/%s) with error: (%s)", retryNum, retry.DefaultDownloadRetryAttempts, containerName, blobName, netErr)
				logger.Log.Warnf("This error is likely unrecoverable, will not retry")
				errorWas404 = true
				closeCtx()
			} else {
				logger.Log.Infof("Attempt %d/%d: failed to download (%s/%s) with error: (%s)", retryNum, retry.DefaultDownloadRetryAttempts, containerName, blobName, netErr)
			}
		}
		retryNum++
		return netErr
	})

	// If the error was a 404-like error, we should not consider the download as cancelled
	if errorWas404 {
		wasCancelled = false
	}

	if err != nil {
		err = fmt.Errorf("failed to download (%s/%s) to (%s):\n%w", containerName, blobName, dstFile, err)
	}
	return
}

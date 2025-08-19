// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package azureblobstorage

import (
	"context"
	"errors"
	"fmt"
	"net/url"
	"os"
	"strings"
	"time"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/Azure/azure-sdk-for-go/sdk/storage/azblob"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

const (
	AnonymousAccess        = 0
	ServicePrincipalAccess = 1
	AzureCLIAccess         = 2
)

// AzureBlobInfo contains parsed information from an Azure Blob Storage URL
type AzureBlobInfo struct {
	StorageAccount string
	ContainerName  string
	BlobName       string
}

// ParseAzureBlobStorageURL parses an Azure Blob Storage URL and extracts storage account information.
func ParseAzureBlobStorageURL(urlStr string) (*AzureBlobInfo, error) {
	parsedURL, err := url.Parse(urlStr)
	if err != nil {
		return nil, fmt.Errorf("failed to parse URL: %w", err)
	}

	if !strings.HasSuffix(parsedURL.Host, ".blob.core.windows.net") {
		return nil, fmt.Errorf("not a common Azure Blob Storage URL format " +
			"(expected <storage_account>.blob.core.windows.net)")
	}

	// Extract storage account from hostname (e.g., "mystorageaccount.blob.core.windows.net")
	hostParts := strings.Split(parsedURL.Host, ".")
	if len(hostParts) < 4 {
		return nil, fmt.Errorf("invalid Azure Blob Storage hostname format")
	}
	storageAccount := hostParts[0]

	// Extract container and blob name from path (e.g., "/container/path/to/blob")
	pathParts := strings.Split(strings.Trim(parsedURL.Path, "/"), "/")
	if len(pathParts) < 2 {
		return nil, fmt.Errorf("invalid Azure Blob Storage path format")
	}

	containerName := pathParts[0]
	blobName := strings.Join(pathParts[1:], "/")

	return &AzureBlobInfo{
		StorageAccount: storageAccount,
		ContainerName:  containerName,
		BlobName:       blobName,
	}, nil
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

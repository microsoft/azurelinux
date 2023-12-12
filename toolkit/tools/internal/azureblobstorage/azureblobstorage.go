// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package azureblobstorage

import (
	"context"
	"errors"
	"fmt"
	"os"
	"time"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/Azure/azure-sdk-for-go/sdk/storage/azblob"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

const (
	AnonymousAccess        = 0
	ServicePrincipalAccess = 1
	ManagedIdentityAccess  = 2
)

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
		return fmt.Errorf("Failed to open local file for upload:\n%w", err)
	}
	defer localFile.Close()

	_, err = abs.theClient.UploadFile(ctx, containerName, blobName, localFile, nil)
	if err != nil {
		return fmt.Errorf("Failed to upload local file to blob:\n%w", err)
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
		return fmt.Errorf("Failed to download blob to local file:\n%w", err)
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
		return fmt.Errorf("Failed to delete blob:\n%w", err)
	}
	deleteEndTime := time.Now()
	logger.Log.Infof("  delete time: %v", deleteEndTime.Sub(deleteStartTime))

	return nil
}

func Create(tenantId string, userName string, password string, storageAccount string, authenticationType int) (abs *AzureBlobStorage, err error) {

	url := "https://" + storageAccount + ".blob.core.windows.net/"

	abs = &AzureBlobStorage{}

	if authenticationType == AnonymousAccess {

		abs.theClient, err = azblob.NewClientWithNoCredential(url, nil)
		if err != nil {
			return nil, fmt.Errorf("Unable to init azure blob storage read-only client:\n%w", err)
		}

		return abs, nil

	} else if authenticationType == ServicePrincipalAccess {

		credential, err := azidentity.NewClientSecretCredential(tenantId, userName, password, nil)
		if err != nil {
			return nil, fmt.Errorf("Unable to init azure service principal identity:\n%w", err)
		}

		abs.theClient, err = azblob.NewClient(url, credential, nil)
		if err != nil {
			return nil, fmt.Errorf("Unable to init azure blob storage read-write client:\n%w", err)
		}

		return abs, nil

	} else if authenticationType == ManagedIdentityAccess {

		credential, err := azidentity.NewDefaultAzureCredential(nil)
		if err != nil {
			return nil, fmt.Errorf("Unable to init azure managed identity:\n%w", err)
		}

		abs.theClient, err = azblob.NewClient(url, credential, nil)
		if err != nil {
			return nil, fmt.Errorf("Unable to init azure blob storage read-write client:\n%w", err)
		}

		return abs, nil

	}

	return nil, errors.New("Unknown authentication type.")
}

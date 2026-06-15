// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package azureblobstorage

import (
	"os"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestParseAzureBlobStorageURL(t *testing.T) {
	tests := []struct {
		name                   string
		urlStr                 string
		wantStorageAccountName string
		wantContainerName      string
		wantBlobName           string
		wantErr                bool
	}{
		{
			name:                   "Valid URL with container only",
			urlStr:                 "https://mystorageaccount.blob.core.windows.net/mycontainer",
			wantStorageAccountName: "mystorageaccount",
			wantContainerName:      "mycontainer",
			wantBlobName:           "",
			wantErr:                false,
		},
		{
			name:                   "Valid URL with container and blob",
			urlStr:                 "https://mystorageaccount.blob.core.windows.net/mycontainer/myblob.txt",
			wantStorageAccountName: "mystorageaccount",
			wantContainerName:      "mycontainer",
			wantBlobName:           "myblob.txt",
			wantErr:                false,
		},
		{
			name:                   "Valid URL with container and blob in folder",
			urlStr:                 "https://mystorageaccount.blob.core.windows.net/mycontainer/folder/myblob.txt",
			wantStorageAccountName: "mystorageaccount",
			wantContainerName:      "mycontainer",
			wantBlobName:           "folder/myblob.txt",
			wantErr:                false,
		},
		{
			name:                   "Valid URL with deep folder hierarchy",
			urlStr:                 "https://mystorageaccount.blob.core.windows.net/mycontainer/folder1/folder2/myfile-1.2.3.tar.gz",
			wantStorageAccountName: "mystorageaccount",
			wantContainerName:      "mycontainer",
			wantBlobName:           "folder1/folder2/myfile-1.2.3.tar.gz",
			wantErr:                false,
		},
		{
			name:                   "Valid URL with trailing slash",
			urlStr:                 "https://mystorageaccount.blob.core.windows.net/mycontainer/",
			wantStorageAccountName: "mystorageaccount",
			wantContainerName:      "mycontainer",
			wantBlobName:           "",
			wantErr:                false,
		},
		{
			name:    "Invalid URL - not Azure Blob Storage format",
			urlStr:  "https://example.com/container/blob",
			wantErr: true,
		},
		{
			name:    "Invalid URL - missing storage account",
			urlStr:  "https://blob.core.windows.net/container/blob",
			wantErr: true,
		},
		{
			name:    "Invalid URL - malformed hostname",
			urlStr:  "https://invalid.hostname/container/blob",
			wantErr: true,
		},
		{
			name:    "Invalid URL - missing container",
			urlStr:  "https://mystorageaccount.blob.core.windows.net/",
			wantErr: true,
		},
		{
			name:    "Invalid URL - empty path",
			urlStr:  "https://mystorageaccount.blob.core.windows.net",
			wantErr: true,
		},
		{
			name:    "Invalid URL - unparseable",
			urlStr:  "not-a-url",
			wantErr: true,
		},
		{
			name:    "Invalid URL - scheme missing",
			urlStr:  "mystorageaccount.blob.core.windows.net/container",
			wantErr: true,
		},
		{
			name:                   "Valid URL with query parameters",
			urlStr:                 "https://mystorageaccount.blob.core.windows.net/mycontainer/myblob.txt?sv=2021-06-08",
			wantStorageAccountName: "mystorageaccount",
			wantContainerName:      "mycontainer",
			wantBlobName:           "myblob.txt",
			wantErr:                false,
		},
		{
			name:                   "Valid URL with special characters in blob name",
			urlStr:                 "https://mystorageaccount.blob.core.windows.net/mycontainer/my-blob_file.2023.txt",
			wantStorageAccountName: "mystorageaccount",
			wantContainerName:      "mycontainer",
			wantBlobName:           "my-blob_file.2023.txt",
			wantErr:                false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			gotStorageAccountName, gotContainerName, gotBlobName, err := ParseAzureBlobStorageURL(tt.urlStr)
			if (err != nil) != tt.wantErr {
				t.Errorf("ParseAzureBlobStorageURL() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if !tt.wantErr {
				if gotStorageAccountName != tt.wantStorageAccountName {
					t.Errorf("ParseAzureBlobStorageURL() gotStorageAccountName = %v, want %v", gotStorageAccountName, tt.wantStorageAccountName)
				}
				if gotContainerName != tt.wantContainerName {
					t.Errorf("ParseAzureBlobStorageURL() gotContainerName = %v, want %v", gotContainerName, tt.wantContainerName)
				}
				if gotBlobName != tt.wantBlobName {
					t.Errorf("ParseAzureBlobStorageURL() gotBlobName = %v, want %v", gotBlobName, tt.wantBlobName)
				}
			}
		})
	}
}

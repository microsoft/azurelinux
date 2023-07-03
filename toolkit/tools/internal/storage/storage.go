// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package storage

import (
	"fmt"

	"golang.org/x/sys/unix"
)

// Units for expressing disk space when calling storage
const (
	KB = 1
	MB = 1024 * KB
	GB = 1024 * MB
)

// CheckDiskSpace checks if the number of 1K blocks available on a
// partition containing a filepath is less than the quota.
func CheckDiskSpace(filepath string, quota int) (err error) {
	var stat unix.Statfs_t
	if err = unix.Statfs(filepath, &stat); err != nil {
		return
	}

	// blocks * block size = available bytes
	sizeInBytes := stat.Bavail * uint64(stat.Bsize)
	availInKbs := sizeInBytes / 1024
	if availInKbs < uint64(quota) {
		err = fmt.Errorf("not enough space on disk containing file %s. Expected %d 1K Blocks found %d", filepath, quota, availInKbs)
	}
	return
}

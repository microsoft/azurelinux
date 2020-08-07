// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package directory

import (
	"os"
	"path/filepath"
	"time"
)

// LastModifiedFile returns the timestamp and path to the file last modified inside a directory.
// Will recursively search.
func LastModifiedFile(dirPath string) (modTime time.Time, latestFile string, err error) {
	err = filepath.Walk(dirPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		currentModTime := info.ModTime()
		if currentModTime.After(modTime) {
			modTime = currentModTime
			latestFile = path
		}

		return nil
	})

	return
}

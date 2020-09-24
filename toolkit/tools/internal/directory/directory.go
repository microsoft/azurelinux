// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package directory

import (
	"os"
	"path/filepath"
	"time"

	"microsoft.com/pkggen/internal/shell"
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

// CopyContents will recursively copy the contents of srcDir into destDir.
// It will create destDir if it does not already exist.
func CopyContents(srcDir, destDir string) (err error) {
	const squashErrors = false

	err = os.MkdirAll(destDir, os.ModePerm)
	if err != nil {
		return
	}

	recursiveSrcDir := filepath.Join(srcDir, "*")

	err = shell.ExecuteLive(squashErrors, "cp", "-r", recursiveSrcDir, destDir)
	return

}

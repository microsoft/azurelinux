// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package directory

import (
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"time"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
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

// CopyContents will recursively copy the contents of srcDir into dstDir.
// - It will create dstDir if it does not already exist.
func CopyContents(srcDir, dstDir string) (err error) {
	const squashErrors = false

	isSrcDir, err := file.IsDir(srcDir)
	if err != nil {
		return err
	}

	if !isSrcDir {
		return fmt.Errorf("source (%s) must be a directory", srcDir)
	}

	err = os.MkdirAll(dstDir, os.ModePerm)
	if err != nil {
		return
	}

	fds, err := ioutil.ReadDir(srcDir)
	if err != nil {
		return
	}

	for _, fd := range fds {
		srcPath := filepath.Join(srcDir, fd.Name())
		dstPath := filepath.Join(dstDir, fd.Name())

		cpArgs := []string{"-a", srcPath, dstPath}
		if fd.IsDir() {
			cpArgs = append([]string{"-r"}, cpArgs...)
		}

		err = shell.ExecuteLive(squashErrors, "cp", cpArgs...)
		if err != nil {
			return
		}
	}
	return
}

func EnsureDirExists(dirName string) (err error) {
	_, err = os.Stat(dirName)
	if err == nil {
		return nil
	}

	if os.IsNotExist(err) {
		err = os.MkdirAll(dirName, 0755)
		if err != nil {
			return err
		}
	} else {
		return err
	}

	return nil
}

func GetChildDirs(parentFolder string) ([]string, error) {
	childFolders := []string{}

	dir, err := os.Open(parentFolder)
	if err != nil {
		return nil, err
	}
	defer dir.Close()

	children, err := dir.Readdirnames(-1)
	if err != nil {
		return nil, err
	}

	for _, child := range children {
		childPath := filepath.Join(parentFolder, child)

		info, err := os.Stat(childPath)
		if err != nil {
			continue
		}

		if info.IsDir() {
			childFolders = append(childFolders, child)
		}
	}

	return childFolders, nil
}

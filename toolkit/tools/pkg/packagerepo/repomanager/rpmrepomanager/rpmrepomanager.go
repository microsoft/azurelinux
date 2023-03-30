// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package rpmrepomanager

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/pkg/shell"
)

// CreateRepo will create an RPM repository at repoDir
func CreateRepo(repoDir string) (err error) {
	const (
		repoDataSubDir = "repodata"
		repoLockSubDir = ".repodata"
	)

	logger.Log.Debugf("Creating RPM repository in (%s)", repoDir)

	repoDataPath := filepath.Join(repoDir, repoDataSubDir)
	repoDataLockPath := filepath.Join(repoDir, repoLockSubDir)

	// Remove the repodata (and the repolock) if exists
	err = os.RemoveAll(repoDataPath)
	if err != nil && !os.IsNotExist(err) {
		return
	}

	err = os.RemoveAll(repoDataLockPath)
	if err != nil && !os.IsNotExist(err) {
		return
	}

	// Create a new repodata
	_, stderr, err := shell.Execute("createrepo", repoDir)
	if err != nil {
		logger.Log.Warn(stderr)
	}

	return
}

// OrganizePackagesByArch will recursively move RPMs from srcDir into architecture folders under repoDir
func OrganizePackagesByArch(srcDir, repoDir string) (err error) {
	const noArch = "noarch"

	logger.Log.Debugf("Organizing RPM packages from (%s) to (%s)", srcDir, repoDir)

	stdout, stderr, err := shell.Execute("uname", "-m")
	if err != nil {
		logger.Log.Warnf("Could not fetch current architecture from shell: %v", stderr)
		return
	}
	currentArch := strings.TrimSpace(stdout)

	didMovePackages := false
	pkgArches := []string{noArch, currentArch}

	for _, arch := range pkgArches {
		var rpmFiles []string

		err = os.MkdirAll(filepath.Join(repoDir, arch), os.ModePerm)
		if err != nil {
			return
		}

		rpmSearch := filepath.Join(srcDir, fmt.Sprintf("*.%s.rpm", arch))
		rpmFiles, err = filepath.Glob(rpmSearch)
		if err != nil {
			return
		}

		for _, rpmFile := range rpmFiles {
			dstFile := filepath.Join(repoDir, arch, filepath.Base(rpmFile))
			err = file.Move(rpmFile, dstFile)
			if err != nil {
				logger.Log.Warnf("Unable to move (%s) to (%s)", rpmFile, dstFile)
				return
			}
		}

		if len(rpmFiles) > 0 {
			didMovePackages = true
		}
	}

	if !didMovePackages {
		logger.Log.Debugf("Failed to locate any downloaded packages. All packages are assumed to be locally available.")
	}

	return
}

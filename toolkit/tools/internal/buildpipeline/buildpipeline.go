// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// tools to handle build pipeline (hence Docker container based pipeline vs regular ones)

package buildpipeline

import (
	"fmt"
	"os"
	"path/filepath"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"

	"golang.org/x/sys/unix"
)

const (
	rootBaseDirEnv = "CHROOT_DIR"
	chrootLock     = "chroot-pool.lock"
	chrootUse      = "chroot-used"
)

// IsRegularBuild indicates if it is a regular build (without using docker)
func IsRegularBuild() bool {
	// some specific build pipeline builds Azure Linux from a Docker container and
	// consequently have special requirements with regards to chroot
	// check if .dockerenv file exist to disambiguate build pipeline
	dockerEnvExists, _ := file.PathExists("/.dockerenv")
	ignoreDockerEnvExists, _ := file.PathExists("/.mariner-toolkit-ignore-dockerenv")
	return ignoreDockerEnvExists || !dockerEnvExists
}

// GetChrootDir returns the chroot folder
//   - proposeDir is suggested folder name
//     in case of Docker based build a chroot dir is selected from the chroot pool and proposeDir is ignored
func GetChrootDir(proposedDir string) (chrootDir string, err error) {
	if IsRegularBuild() {
		// don't change proposed dir in case of regular build
		return proposedDir, nil
	}

	// In docker based pipeline pre-existing chroot pool is under a folder which path
	// is indicated by an env variable
	chrootPoolFolder, varExist := unix.Getenv(rootBaseDirEnv)
	if !varExist || len(chrootPoolFolder) == 0 {
		err = fmt.Errorf("env variable (%s) not defined", rootBaseDirEnv)
		logger.Log.Errorf("%s", err.Error())
		return "", err
	}

	// lock chroot pool (multi-process lock mechanism)
	chrootLockFile := filepath.Join(chrootPoolFolder, chrootLock)
	flock, err := os.Open(chrootLockFile)
	if err != nil {
		logger.Log.Errorf("Failed to open chroot pool lock (%s) - %s", chrootLockFile, err.Error())
		return "", err
	}
	defer flock.Close()

	err = unix.Flock(int(flock.Fd()), unix.LOCK_EX)
	if err != nil {
		logger.Log.Errorf("Failed to lock (%s) - %s", chrootLockFile, err.Error())
		return "", err
	}
	defer unix.Flock(int(flock.Fd()), unix.LOCK_UN)

	// get list of chroots inside chroot pool and found one which is available
	// nNote that a chroot is currently in use if 'chrootUse' file exist hence is available for use
	// if that file doesn't exist
	chrootDirs, err := os.Open(chrootPoolFolder)
	if err != nil {
		logger.Log.Errorf("Failed to open chroot pool folder (%s) - %s", chrootPoolFolder, err.Error())
		return "", err
	}
	defer chrootDirs.Close()

	names, err := chrootDirs.Readdirnames(-1)
	if err != nil {
		logger.Log.Errorf("Failed to get subfolder in chroot pool folder (%s) - %s", chrootPoolFolder, err.Error())
		return "", err
	}

	for _, name := range names {
		fullChrootPath := filepath.Join(chrootPoolFolder, name)

		isDir, _ := file.IsDir(fullChrootPath)
		if isDir {
			// check if chroot is in use
			inUseFilePath := filepath.Join(fullChrootPath, chrootUse)
			_, err := os.Stat(inUseFilePath)
			if err == nil {
				// chroot in use => check next
				logger.Log.Debugf("chroot (%s) currently used", fullChrootPath)
				continue
			} else if os.IsNotExist(err) {
				// chroot not in use
				inUseFile, err := os.Create(inUseFilePath)
				if err != nil {
					logger.Log.Errorf("Cannot indicate that chroot (%s) is now used - %s", fullChrootPath, err.Error())
					return "", err
				}

				logger.Log.Debugf("Select chroot -> %s", fullChrootPath)
				defer inUseFile.Close()
				return fullChrootPath, nil
			} else {
				logger.Log.Errorf("Cannot read chroot status file (%s) - %s", inUseFilePath, err.Error())
				return "", err
			}
		}
	}

	err = fmt.Errorf("no chroot available in %s", chrootPoolFolder)
	logger.Log.Error(err.Error())
	return "", err
}

// ReleaseChrootDir releases a chroot dir
// note that this routine does nothing case of regular build
func ReleaseChrootDir(chrootDir string) (err error) {
	if IsRegularBuild() {
		// nothing to do in case of regular build
		return
	}

	// sanity check
	if len(chrootDir) == 0 {
		err = fmt.Errorf("try to release unamed chroot")
		logger.Log.Errorf("%s", err.Error())
		return
	}

	// In docker based pipeline pre-existing chroot pool is under a folder which path
	// is indicated by an env variable
	chrootPoolFolder, varExist := unix.Getenv(rootBaseDirEnv)
	if !varExist || len(chrootPoolFolder) == 0 {
		err = fmt.Errorf("env variable (%s) not defined", rootBaseDirEnv)
		logger.Log.Errorf("%s", err.Error())
		return
	}

	// lock chroot pool (multi-process lock mechanism)
	chrootLockFile := filepath.Join(chrootPoolFolder, chrootLock)
	flock, err := os.Open(chrootLockFile)
	if err != nil {
		logger.Log.Errorf("Failed to open chroot pool lock (%s) - %s", chrootLockFile, err.Error())
		return
	}
	defer flock.Close()

	err = unix.Flock(int(flock.Fd()), unix.LOCK_EX)
	if err != nil {
		logger.Log.Errorf("Failed to lock (%s) - %s", chrootLockFile, err.Error())
		return
	}
	defer unix.Flock(int(flock.Fd()), unix.LOCK_UN)

	// release chroot
	logger.Log.Debugf("Release chroot -> %s", filepath.Join(chrootDir, chrootUse))
	err = os.Remove(filepath.Join(chrootDir, chrootUse))
	if err != nil {
		logger.Log.Errorf("Failed to remove (%s) - %s", filepath.Join(chrootDir, chrootUse), err.Error())
		return
	}

	return
}

// GetRpmsDir returns the RPMS folder
// - proposeDir is suggested folder name and will be ignored in case of Docker based build
func GetRpmsDir(chrootDir string, proposedDir string) string {
	if IsRegularBuild() {
		// just join chroot dir and proposed dir in case of regular build
		return filepath.Join(chrootDir, proposedDir)
	}

	// In Docker based pipeline RPMS folder is always located under the localrpms folder
	return filepath.Join(chrootDir, "localrpms")
}

// CleanupDockerChroot: Docker based only, clean chroot =>
//  1. delete everything but the folders listed
//     these folders are the ones mounted in docker run command (-v option)
//  2. create empty folders
//     these folders are required by chroot (e.g.: /run) and needs to be created empty
//     to not inherit anything from previous build
func CleanupDockerChroot(chroot string) (err error) {
	var folderToKeep = []string{
		"dev",
		"ccache-dir",
		"proc",
		"localrpms",
		"toolchainrpms",
		"upstream-cached-rpms",
		"sys",
		chrootUse,
	}

	var folderToCreate = []string{
		"run",
	}

	logger.Log.Debugf("cleanup Chroot -> %s", chroot)

	rootFolder, err := os.Open(chroot)
	if err != nil {
		logger.Log.Warnf("Open chroot (%s) failed - %s", chroot, err)
		return err
	}

	defer rootFolder.Close()
	names, err := rootFolder.Readdirnames(-1)
	if err != nil {
		logger.Log.Warnf("Reading files and folders under chroot (%s) failed - %s", chroot, err)
		return err
	}

	for _, name := range names {
		var toDelete = true
		for _, folder := range folderToKeep {
			if name == folder {
				toDelete = false
				break
			}
		}
		if toDelete {
			err = os.RemoveAll(filepath.Join(chroot, name))
			if err != nil {
				logger.Log.Warnf("Removing files in chroot (%s) failed: %s", chroot, err)
			}
		}
	}

	// create some folder(s) once chroot has been cleaned up
	for _, folder := range folderToCreate {
		err = os.Mkdir(filepath.Join(chroot, folder), os.ModePerm)
		if err != nil {
			logger.Log.Warnf("Creation of (%s) folder in chroot (%s) failed: %s", folder, chroot, err)
		}
	}

	return
}

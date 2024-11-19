// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// tools to handle build pipeline (hence Docker container based pipeline vs regular ones)

package buildpipeline

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	"github.com/sirupsen/logrus"
	"golang.org/x/sys/unix"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

const (
	rootBaseDirEnv        = "CHROOT_DIR"
	chrootLock            = "chroot-pool.lock"
	chrootUse             = "chroot-used"
	systemdDetectVirtTool = "systemd-detect-virt"
)

var isRegularBuildCached *bool

// checkIfContainerDockerEnvFile checks if the tool is running in a Docker container by checking if /.dockerenv exists. This
// check may not be reliable in all environments, so it is recommended to use systemd-detect-virt if available.
func checkIfContainerDockerEnvFile() (bool, error) {
	exists, err := file.PathExists("/.dockerenv")
	if err != nil {
		err = fmt.Errorf("failed to check if /.dockerenv exists:\n%w", err)
		return false, err
	}
	return exists, nil
}

// checkIfContainerIgnoreDockerEnvFile checks if the user has placed a file in the root directory to ignore the Docker
// environment check.
func checkIfContainerIgnoreDockerEnvFile() (bool, error) {
	ignoreDockerEnvExists, err := file.PathExists("/.mariner-toolkit-ignore-dockerenv")
	if err != nil {
		err = fmt.Errorf("failed to check if /.mariner-toolkit-ignore-dockerenv exists:\n%w", err)
		return false, err
	}
	return ignoreDockerEnvExists, nil
}

// checkIfContainerChrootDirEnv checks if the user has set the CHROOT_DIR environment variable, which is a requirement for
// Docker-based builds. If the variable exists, it is likely that the tool is running in a Docker container.
func checkIfContainerChrootDirEnv() bool {
	_, exists := os.LookupEnv(rootBaseDirEnv)
	return exists
}

// checkIfContainerSystemdDetectVirt uses systemd-detect-virt, a tool that can be used to detect if the system is running
// in a virtualized environment. More specifically, using '-c' flag will detect container-based virtualization only.
func checkIfContainerSystemdDetectVirt() (bool, error) {
	// We should have the systemd-detect-virt command available in the environment, but check for it just in case since it
	// was previously not explicitly required for the toolkit.
	_, err := exec.LookPath(systemdDetectVirtTool)
	if err != nil {
		err = fmt.Errorf("failed to find %s in the PATH:\n%w", systemdDetectVirtTool, err)
		return false, err
	}

	// The tool will return error code 1 based on detection, we only care about the stdout so ignore the return code.
	stdout, _, _ := shell.Execute(systemdDetectVirtTool, "-c")

	// There are several possible outputs from systemd-detect-virt we care about:
	// - none: Not running in a virtualized environment, easy
	// - wsl: Reports as a container, but we don't want to treat it as such. It should be able to handle regular builds
	// - anything else: We'll assume it's a container
	stdout = strings.TrimSpace(stdout)
	switch stdout {
	case "none":
		logger.Log.Debugf("Tool is not running in a container, systemd-detect-virt reports: '%s'", stdout)
		return false, nil
	case "wsl":
		logger.Log.Debugf("Tool is running in WSL, treating as a non-container environment, systemd-detect-virt reports: '%s'", stdout)
		return false, nil
	default:
		logger.Log.Debugf("Tool is running in a container, systemd-detect-virt reports: '%s'", stdout)
		return true, nil
	}
}

// IsRegularBuild indicates if it is a regular build (without using docker)
func IsRegularBuild() bool {
	if isRegularBuildCached != nil {
		return *isRegularBuildCached
	}

	// If /.mariner-toolkit-ignore-dockerenv exists, then it is a regular build no matter what.
	hasIgnoreFile, err := checkIfContainerIgnoreDockerEnvFile()
	if err != nil {
		// Log the error, but continue with the check.
		logger.Log.Warnf("Failed to check if /.mariner-toolkit-ignore-dockerenv exists: %s", err)
	}
	if hasIgnoreFile {
		isRegularBuild := true
		isRegularBuildCached = &isRegularBuild
		return isRegularBuild
	}

	// There are multiple ways to detect if the build is running in a Docker container.
	// - Check with systemd-detect-virt tool first. This is the most reliable way.
	// - The legacy way is to check if /.dockerenv exists. However, this is not reliable
	//   as it may not be present in all environments.
	// - If the user has set the CHROOT_DIR environment variable, then it is likely a Docker build.
	isRegularBuild := true
	isDockerContainer, err := checkIfContainerSystemdDetectVirt()
	if err == nil {
		isRegularBuild = !isDockerContainer
		if !isRegularBuild {
			logger.Log.Info("systemd-detect-virt reports that the tool is running in a container, running as a container build")
		}
	} else {
		// Fallback if systemd-detect-virt isn't available.
		isDockerContainer, err = checkIfContainerDockerEnvFile()
		if err != nil {
			// Log the error, but continue with the check.
			logger.Log.Warnf("Failed to check if /.dockerenv exists: %s", err)
		} else {
			isRegularBuild = !isDockerContainer
		}
		message := []string{
			"Failed to detect if the system is running in a container using systemd-detect-virt.",
			err.Error(),
			"Checking if the system is running in a container by checking /.dockerenv.",
		}
		if isRegularBuild {
			message = append(message, "Result: Not a container.")
		} else {
			message = append(message, "Result: Container detected.")
		}
		logger.PrintMessageBox(logrus.WarnLevel, message)
	}

	// If the user set the CHROOT_DIR environment variable, but we don't detect a container, print a warning. This is
	// likely a misconfiguration, however trust the user and force the build to run as a container. If this is a mistake,
	// the tools should fail very quickly after this point.
	if checkIfContainerChrootDirEnv() && isRegularBuild {
		message := []string{
			"CHROOT_DIR is set, but the system is not detected as a container.",
			"This is likely a misconfiguration!",
			"**Forcing the build to run as a container build**, however chroot operations may fail.",
		}
		logger.PrintMessageBox(logrus.WarnLevel, message)
		isRegularBuild = false
	}

	// Cache the result
	isRegularBuildCached = &isRegularBuild
	return isRegularBuild
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
	chrootPoolFolder, varExist := os.LookupEnv(rootBaseDirEnv)
	if !varExist || len(chrootPoolFolder) == 0 {
		err = fmt.Errorf("env variable %s not defined", rootBaseDirEnv)
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
				logger.Log.Debugf("chroot %s currently used", fullChrootPath)
				continue
			} else if os.IsNotExist(err) {
				// chroot not in use
				inUseFile, err := os.Create(inUseFilePath)
				if err != nil {
					logger.Log.Errorf("Cannot indicate that chroot %s is now used - %s", fullChrootPath, err.Error())
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
		err = fmt.Errorf("env variable %s not defined", rootBaseDirEnv)
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
		logger.Log.Errorf("Failed to remove %s - %s", filepath.Join(chrootDir, chrootUse), err.Error())
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
		logger.Log.Warnf("Open chroot %s failed - %s", chroot, err)
		return err
	}

	defer rootFolder.Close()
	names, err := rootFolder.Readdirnames(-1)
	if err != nil {
		logger.Log.Warnf("Reading files and folders under chroot %s failed - %s", chroot, err)
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
				logger.Log.Warnf("Removing files in chroot %s failed: %s", chroot, err)
			}
		}
	}

	// create some folder(s) once chroot has been cleaned up
	for _, folder := range folderToCreate {
		err = os.Mkdir(filepath.Join(chroot, folder), os.ModePerm)
		if err != nil {
			logger.Log.Warnf("Creation of %s folder in chroot %s failed: %s", folder, chroot, err)
		}
	}

	return
}

// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's PackageRepo configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
	"net/url"
	"os"
	"path/filepath"
	"strings"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/network"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/safechroot"
	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/shell"
)

// PackageRepo defines the RPM repo to pull packages from during the installation
// or after the system is installed. The "Install" option indicates that the provided
// repository configuration will be saved in the installed system if specified, and only
// available during the installation process if not
type PackageRepo struct {
	Name     string `json:"Name"`
	BaseUrl  string `json:"BaseUrl"`
	Install  bool   `json:"Install"`
	GPGCheck bool   `json:"GPGCheck"` // Default value is true
	GPGKeys  string `json:"GPGKeys"`  // Default value is "file:///etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY file:///etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY"
}

func getDefaultGPGCheck() bool {
	return true
}

func getDefaultGPGKeys() string {
	return "file:///etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY file:///etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY"
}

// UnmarshalJSON Unmarshals a PackageRepo entry
func (p *PackageRepo) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypePackageRepo PackageRepo

	// Set default values
	p.GPGCheck = getDefaultGPGCheck()
	p.GPGKeys = getDefaultGPGKeys()

	err = json.Unmarshal(b, (*IntermediateTypePackageRepo)(p))
	if err != nil {
		return fmt.Errorf("failed to parse [PackageRepo]: %w", err)
	}

	// Now validate the resulting unmarshaled object
	err = p.IsValid()
	if err != nil {
		return fmt.Errorf("failed to parse [PackageRepo]: %w", err)
	}
	return
}

// IsValid returns an error if the PackageRepo struct is not valid
func (p *PackageRepo) IsValid() (err error) {
	err = p.nameIsValid()
	if err != nil {
		return
	}

	err = p.repoUrlIsValid()
	if err != nil {
		return
	}

	// Repos for ISO use only (install = false) cannot support custom GPG keys if GPGCheck is enabled. Warn the user even
	// if we are installing the repo file, as the repo file will not be usable in the installer.
	if p.GPGCheck && p.GPGKeys != getDefaultGPGKeys() {
		if !p.Install {
			err = fmt.Errorf("invalid value for package repo '%s' [GPGKeys] (%s), custom GPG keys are only supported for repos that are installed", p.Name, p.GPGKeys)
			return
		} else {
			logger.Log.Warnf("Warning: Custom GPG keys are only supported for repos that are installed. The repo file for '%s' will not be usable in the installer.", p.Name)
		}
	}

	return
}

// UpdatePackageRepo creates additional repo files specified by image configuration
// and returns error if the operation fails
func UpdatePackageRepo(installChroot *safechroot.Chroot, config SystemConfig) (err error) {
	const (
		repoFileDir   = "/etc/yum.repos.d/"
		localRepoFile = "/etc/yum.repos.d/mariner-iso.repo"
		squashErrors  = false
	)

	if exists, ferr := file.DirExists(repoFileDir); ferr != nil {
		logger.Log.Errorf("Error accessing repo file directory %s.", repoFileDir)
		err = ferr
		return
	} else if !exists {
		err = fmt.Errorf("Could not find the repo file directory %s to update package repo", repoFileDir)
		return
	}

	// Remove mariner-iso.repo
	os.Remove(localRepoFile)

	// Clean up all newly created package repo files in case there's any
	// repo file creation error
	defer func() {
		// Delete all files under /etc/yum.repos.d/
		if err != nil {
			err = shell.ExecuteLive(squashErrors, "rm", fmt.Sprintf("%s/*", repoFileDir))
			if err != nil {
				logger.Log.Errorf("Failed to clean up repo files under %s. Error: %s", repoFileDir, err)
			}
		}
	}()

	// Loop through the PackageRepos field to determine if any customized package repos are specified.
	// If specified, create new repo files for them
	for _, packageRepo := range config.PackageRepos {
		err = createCustomPackageRepo(installChroot, packageRepo, repoFileDir)
		if err != nil {
			return
		}
	}

	// It is possible that network access may not be up at this point,
	// so check network access
	err, hasNetworkAccess := network.CheckNetworkAccess()
	if err != nil {
		return
	}
	if !hasNetworkAccess {
		err = fmt.Errorf("no network access in the system")
	}
	return
}

// nameIsValid returns an error if the package repo name is empty
func (p *PackageRepo) nameIsValid() (err error) {
	if strings.TrimSpace(p.Name) == "" {
		return fmt.Errorf("invalid value for package repo [Name] (%s), name cannot be empty", p.Name)
	}
	return
}

// repoUrlIsValid returns an error if the package url is invalid
func (p *PackageRepo) repoUrlIsValid() (err error) {
	if strings.TrimSpace(p.BaseUrl) == "" {
		return fmt.Errorf("invalid value for package repo [BaseUrl] (%s), URL cannot be empty", p.BaseUrl)
	}

	_, err = url.ParseRequestURI(p.BaseUrl)
	if err != nil {
		logger.Log.Errorf("Failed to parse input URL %s, Error: %s", p.BaseUrl, err)
	}
	return
}

func writeAdditionalFields(stringBuilder *strings.Builder) (err error) {
	const (
		enable       = "enabled=1\n"
		repogpgCheck = "repo_gpgcheck=1\n"
		skip         = "skip_if_unavailable=True\n"
		sslVerify    = "sslverify=1\n"
	)

	additionalFields := []string{enable, repogpgCheck, skip, sslVerify}

	for _, additionalField := range additionalFields {
		_, err = stringBuilder.WriteString(additionalField)
		if err != nil {
			logger.Log.Errorf("Error writing additional field '%s' out of all fields: %s. Error: %s", additionalField, additionalFields, err)
			return
		}
	}

	return
}

func createCustomRepoFile(fileName string, packageRepo PackageRepo) (err error) {
	var stringBuilder strings.Builder

	err = file.Create(fileName, 0644)
	if err != nil {
		logger.Log.Errorf("Error creating file (%s)", fileName)
		return
	}

	defer func() {
		// Delete the repo file on failure
		if err != nil {
			err = os.Remove(fileName)
			if err != nil {
				logger.Log.Errorf("Failed to clean up repo file: %s. Error: %s", fileName, err)
			}
		}
	}()

	// Write the repo identifier field
	repoId := fmt.Sprintf("[%s]\n", packageRepo.Name)
	_, err = stringBuilder.WriteString(repoId)
	if err != nil {
		logger.Log.Errorf("Error writing repo ID: %s. Error: %s", repoId, err)
		return
	}

	// Write the repo Name field
	repoName := fmt.Sprintf("name=%s\n", packageRepo.Name)
	_, err = stringBuilder.WriteString(repoName)
	if err != nil {
		logger.Log.Errorf("Error writing repo Name: %s. Error: %s", repoName, err)
		return
	}

	// Write the repo URL field
	repoUrl := fmt.Sprintf("baseurl=%s\n", packageRepo.BaseUrl)
	_, err = stringBuilder.WriteString(repoUrl)
	if err != nil {
		logger.Log.Errorf("Error writing repo URL: %s. Error: %s", repoUrl, err)
		return
	}

	// Write the GPGKey field
	gpgKey := fmt.Sprintf("gpgkey=%s\n", packageRepo.GPGKeys)
	_, err = stringBuilder.WriteString(gpgKey)
	if err != nil {
		logger.Log.Errorf("Error writing repo GPGKey: %s. Error: %s", gpgKey, err)
		return
	}

	// Write the repo GPGCheck field
	var gpgVal string
	if packageRepo.GPGCheck {
		gpgVal = "1"
	} else {
		gpgVal = "0"
	}
	repoGpgCheck := fmt.Sprintf("gpgcheck=%s\n", gpgVal)
	_, err = stringBuilder.WriteString(repoGpgCheck)
	if err != nil {
		logger.Log.Errorf("Error writing repo GPGCheck: %s. Error: %s", repoGpgCheck, err)
		return
	}

	// Write additional fields, gpg key etc.
	err = writeAdditionalFields(&stringBuilder)
	if err != nil {
		return
	}

	err = file.Append(stringBuilder.String(), fileName)
	return
}

func createCustomPackageRepo(installChroot *safechroot.Chroot, packageRepo PackageRepo, repoFileDir string) (err error) {
	dstRepoPath := filepath.Join(repoFileDir, packageRepo.Name+".repo")

	// Create repo file
	err = createCustomRepoFile(dstRepoPath, packageRepo)
	if err != nil {
		return
	}

	// Check the repo file needs to be installed in the image
	if packageRepo.Install {
		installRepoFile := filepath.Join(installChroot.RootDir(), dstRepoPath)
		err = file.Copy(dstRepoPath, installRepoFile)
	}

	return
}

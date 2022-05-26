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
)

// PackageRepo defines the RPM repo to pull packages from during the installation
// or after the system is installed. The "Install" option indicates that the provided
// repository configuration will be saved in the installed system if specified, and only
// available during the installation process if not
type PackageRepo struct {
	Name    string `json:"Name"`
	BaseUrl string `json:"BaseUrl"`
	Install bool   `json:"Install"`
}

// UnmarshalJSON Unmarshals a PackageRepo entry
func (p *PackageRepo) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypePackageRepo PackageRepo
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
	err = network.CheckNetworkAccess()
	return
}

// nameIsValid returns an error if the package repo name is empty
func (p *PackageRepo) nameIsValid() (err error) {
	if strings.TrimSpace(p.Name) == "" {
		return fmt.Errorf("invalid value for package repo name (%s), name cannot be empty", p.Name)
	}
	return
}

// repoUrlIsValid returns an error if the package url is invalid
func (p *PackageRepo) repoUrlIsValid() (err error) {
	if strings.TrimSpace(p.BaseUrl) == "" {
		return fmt.Errorf("invalid value for package repo URL (%s), URL cannot be empty", p.BaseUrl)
	}

	_, err = url.ParseRequestURI(p.BaseUrl)
	return
}

func writeAdditionalFields(stringBuilder *strings.Builder) (err error) {
	const (
		gpgKey       = "gpgkey=file:///etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY file:///etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY\n"
		enable       = "enabled=1\n"
		gpgCheck     = "gpgcheck=1\n"
		repogpgCheck = "repo_gpgcheck=1\n"
		skip         = "skip_if_unavailable=True\n"
		sslVerify    = "sslverify=1\n"
	)

	additionalFields := gpgKey + enable + gpgCheck + repogpgCheck + skip + sslVerify
	_, err = stringBuilder.WriteString(additionalFields)
	if err != nil {
		logger.Log.Errorf("Error writing additional fields: %s. Error: %s", additionalFields, err)
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

	defer func() {
		// Delete the repo file on failure
		if err != nil {
			err = os.Remove(dstRepoPath)
			if err != nil {
				logger.Log.Errorf("Failed to clean up repo file: %s. Error: %s", dstRepoPath, err)
			}
		}
	}()

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

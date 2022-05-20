// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// Parser for the image builder's PackageRepo configuration schemas.

package configuration

import (
	"encoding/json"
	"fmt"
	"net/url"
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
	err = p.NameIsValid()
	if err != nil {
		return
	}

	err = p.RepoUrlIsValid()
	if err != nil {
		return
	}

	return
}

// NameIsValid returns an error if the package repo name is empty
func (p *PackageRepo) NameIsValid() (err error) {
	if strings.TrimSpace(p.Name) == "" {
		return fmt.Errorf("invalid value for package repo name (%s), name cannot be empty", p.Name)
	}
	return
}

// RepoUrlIsValid returns an error if the package url is invalid
func (p *PackageRepo) RepoUrlIsValid() (err error) {
	if strings.TrimSpace(p.BaseUrl) == "" {
		return fmt.Errorf("invalid value for package repo URL (%s), URL cannot be empty", p.BaseUrl)
	}

	_, err = url.ParseRequestURI(p.BaseUrl)
	if err != nil {
		return
	}
	return
}

func writeAdditionalFieldstoRepoFile(fileName string) (err error) {
	const (
		gpgKey    = "gpgkey=file:///etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY file:///etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY\n"
		enable    = "enabled=1\n"
		gpgCheck  = "gpgcheck=0\n"
		skip      = "skip_if_unavailable=True\n"
		sslVerify = "sslverify=0\n"
	)

	additionalFields := gpgKey + enable + gpgCheck + skip + sslVerify
	err = file.Append(additionalFields, fileName)
	if err != nil {
		logger.Log.Errorf("Failed to write additional fields")
	}

	return
}

func createCustomRepoFile(fileName string, packageRepo PackageRepo) (err error) {
	err = file.Create(fileName, 0644)
	if err != nil {
		logger.Log.Errorf("Error creating file %s", fileName)
		return
	}

	// Write the repo identifier field
	repoId := "[" + packageRepo.Name + "]\n"
	err = file.Append(repoId, fileName)
	if err != nil {
		logger.Log.Errorf("Failed to write repo identifier %s", repoId)
		return
	}

	// Write the repo Name field
	repoName := "name=" + packageRepo.Name + " $releasever $basearch\n"
	err = file.Append(repoName, fileName)
	if err != nil {
		logger.Log.Errorf("Failed to write repo name %s", repoName)
		return
	}

	// Write the repo URL field
	repoUrl := "baseurl=" + packageRepo.BaseUrl + "\n"
	err = file.Append(repoUrl, fileName)
	if err != nil {
		logger.Log.Errorf("Failed to write repo URL %s", repoUrl)
		return
	}

	err = writeAdditionalFieldstoRepoFile(fileName)
	return
}

func createCustomPackageRepo(installChroot *safechroot.Chroot, packageRepo PackageRepo, repoFileDir string) (err error) {

	dstRepoPath := filepath.Join(repoFileDir, packageRepo.Name + ".repo")

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

// UpdatePackageRepo creates additional repo files specified by image configuration
// and returns error if the operation fails
func UpdatePackageRepo(installChroot *safechroot.Chroot, config SystemConfig) (err error) {
	const (
		repoFileDir   = "/etc/yum.repos.d/"
		localRepoFile = "/etc/yum.repos.d/mariner-iso.repo"
		squashErrors  = false
	)

	if exists, ferr := file.DirExists(repoFileDir); ferr != nil {
		logger.Log.Errorf("Error accessing repo file directory.")
		err = ferr
		return
	} else if !exists {
		err = fmt.Errorf("%s: no such directory", repoFileDir)
		return
	}

	// Remove mariner-iso.repo
	if exists, ferr := file.PathExists(localRepoFile); ferr != nil {
		logger.Log.Errorf("Error accessing /etc/yum.repos.d/mariner-iso.repo")
		err = ferr
		return
	} else if !exists {
		err = fmt.Errorf("%s: no such file or directory", localRepoFile)
		return
	}

	err = shell.ExecuteLive(squashErrors, "rm", localRepoFile)
	if err != nil {
		return
	}

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

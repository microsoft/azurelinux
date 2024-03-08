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

	"github.com/microsoft/azurelinux/toolkit/tools/internal/file"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/network"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/safechroot"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/shell"
)

// PackageRepo defines the RPM repo to pull packages from during the installation
// or after the system is installed. The "Install" option indicates that the provided
// repository configuration will be saved in the installed system if specified, and only
// available during the installation process if not
type PackageRepo struct {
	Name         string `json:"Name"`
	BaseUrl      string `json:"BaseUrl"`
	Install      bool   `json:"Install"`
	GPGCheck     bool   `json:"GPGCheck"`     // Default value is true
	RepoGPGCheck bool   `json:"RepoGPGCheck"` // Default value is true
	GPGKeys      string `json:"GPGKeys"`      // Default value is "file:///etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY file:///etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY"
}

const (
	packageRepoDefaultGPGCheck     = true
	packageRepoDefaultRepoGPGCheck = true
	packageRepoDefaultGPGKeys      = "file:///etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY file:///etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY"
)

// UnmarshalJSON Unmarshals a PackageRepo entry
func (p *PackageRepo) UnmarshalJSON(b []byte) (err error) {
	// Use an intermediate type which will use the default JSON unmarshal implementation
	type IntermediateTypePackageRepo PackageRepo

	// Set default values
	p.GPGCheck = packageRepoDefaultGPGCheck
	p.RepoGPGCheck = packageRepoDefaultRepoGPGCheck
	p.GPGKeys = packageRepoDefaultGPGKeys

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

	// Repos for ISO use only (install = false) cannot support custom GPG keys if GPGCheck/RepoGPGCheck is enabled. Warn the user even
	// if we are installing the repo file, as the repo file will not be usable in the installer.
	if (p.GPGCheck || p.RepoGPGCheck) && p.GPGKeys != packageRepoDefaultGPGKeys {
		if !p.Install {
			err = fmt.Errorf("invalid value for package repo (%s) [GPGKeys] (%s), custom GPG keys are only supported for repos that are installed into the final image by setting 'Install=true'", p.Name, p.GPGKeys)
			return
		} else {
			logger.Log.Warnf("Warning: Custom GPG keys are only supported for repos that are installed into the final image after the ISO runs. The repo file for (%s) will not be usable during the installation process.", p.Name)
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
		err = fmt.Errorf("failed to access repo file directory (%s):\n%w", repoFileDir, ferr)
		return
	} else if !exists {
		err = fmt.Errorf("failed to find the repo file directory (%s) to update package repo", repoFileDir)
		return
	}

	// Remove mariner-iso.repo
	os.Remove(localRepoFile)

	// Clean up all newly created package repo files in case there's any
	// repo file creation error
	defer func() {
		// Delete all files under /etc/yum.repos.d/
		if err != nil {
			cleanupErr := shell.ExecuteLive(squashErrors, "rm", fmt.Sprintf("%s/*", repoFileDir))
			if cleanupErr != nil {
				err = fmt.Errorf("%w\ncleanup-error: failed to clean up repo files under (%s):\n%w", err, repoFileDir, cleanupErr)
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
		return fmt.Errorf("failed to parse input URL (%s):\n%w", p.BaseUrl, err)
	}
	return
}

func writeAdditionalFields(stringBuilder *strings.Builder) (err error) {
	const (
		enable    = "enabled=1\n"
		skip      = "skip_if_unavailable=True\n"
		sslVerify = "sslverify=1\n"
	)

	additionalFields := []string{enable, skip, sslVerify}

	for _, additionalField := range additionalFields {
		_, err = stringBuilder.WriteString(additionalField)
		if err != nil {
			return fmt.Errorf("failed to write additional field (%s) out of all fields (%s):\n%w", additionalField, additionalFields, err)
		}
	}

	return
}

// convertBoolToRepoFlag converts a boolean value to a string that can be used in a repo file. It will be of the
// form "key=1" or "key=0".
func convertBoolToRepoFlag(key string, value bool) string {
	if value {
		return fmt.Sprintf("%s=1\n", key)
	} else {
		return fmt.Sprintf("%s=0\n", key)
	}
}

func createCustomRepoFile(fileName string, packageRepo PackageRepo) (err error) {
	var stringBuilder strings.Builder

	err = file.Create(fileName, 0644)
	if err != nil {
		return fmt.Errorf("failed to create file (%s):\n%w", fileName, err)
	}

	defer func() {
		// Delete the repo file on failure
		if err != nil {
			cleanupErr := os.Remove(fileName)
			if cleanupErr != nil {
				err = fmt.Errorf("%w\ncleanup-error: failed to clean up repo file (%s):\n%w", err, fileName, cleanupErr)
			}
		}
	}()

	// Write the repo identifier field
	repoId := fmt.Sprintf("[%s]\n", packageRepo.Name)
	_, err = stringBuilder.WriteString(repoId)
	if err != nil {
		err = fmt.Errorf("failed to write repo ID (%s):\n%w", repoId, err)
		return
	}

	// Write the repo Name field
	repoName := fmt.Sprintf("name=%s\n", packageRepo.Name)
	_, err = stringBuilder.WriteString(repoName)
	if err != nil {
		err = fmt.Errorf("failed to write repo Name (%s):\n%w", repoName, err)
		return
	}

	// Write the repo URL field
	repoUrl := fmt.Sprintf("baseurl=%s\n", packageRepo.BaseUrl)
	_, err = stringBuilder.WriteString(repoUrl)
	if err != nil {
		err = fmt.Errorf("failed to write repo URL (%s):\n%w", repoUrl, err)
		return
	}

	// Write the GPGKey field
	gpgKey := fmt.Sprintf("gpgkey=%s\n", packageRepo.GPGKeys)
	_, err = stringBuilder.WriteString(gpgKey)
	if err != nil {
		err = fmt.Errorf("failed to write repo GPGKey (%s):\n%w", gpgKey, err)
		return
	}

	// Write the  GPGCheck field
	_, err = stringBuilder.WriteString(convertBoolToRepoFlag("gpgcheck", packageRepo.GPGCheck))
	if err != nil {
		err = fmt.Errorf("failed to write GPGCheck:\n%w", err)
		return
	}

	// Write the repo GPGCheck field
	_, err = stringBuilder.WriteString(convertBoolToRepoFlag("repo_gpgcheck", packageRepo.RepoGPGCheck))
	if err != nil {
		err = fmt.Errorf("failed to write repo RepoGPGCheck:\n%w", err)
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

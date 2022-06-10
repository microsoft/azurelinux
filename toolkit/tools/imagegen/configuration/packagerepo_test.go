// Copyright Microsoft Corporation.
// Licensed under the MIT License.

package configuration

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/file"
	"github.com/stretchr/testify/assert"
)

// TestMain found in configuration_test.go.

var (
	validPackageRepos = []PackageRepo{
		{
			Name:    "mariner-official-base",
			BaseUrl: "https://packages.microsoft.com/cbl-mariner/$releasever/prod/base/$basearch",
			Install: false,
		},
		{
			Name:    "mariner-official-preview",
			BaseUrl: "https://packages.microsoft.com/cbl-mariner/$releasever/preview/base/$basearch",
			Install: true,
		},
	}

	validRepoContent = []string{
		"[mariner-official-base]",
		"name=mariner-official-base",
		"baseurl=https://packages.microsoft.com/cbl-mariner/$releasever/prod/base/$basearch",
		"gpgkey=file:///etc/pki/rpm-gpg/MICROSOFT-RPM-GPG-KEY file:///etc/pki/rpm-gpg/MICROSOFT-METADATA-GPG-KEY",
		"enabled=1",
		"gpgcheck=1",
		"repo_gpgcheck=1",
		"skip_if_unavailable=True",
		"sslverify=1",
	}
)

func TestShouldPassParsingValidPackageRepos_PackageRepo(t *testing.T) {
	for _, p := range validPackageRepos {
		var checkedPackageRepo PackageRepo
		assert.NoError(t, p.IsValid())
		err := remarshalJSON(p, &checkedPackageRepo)
		assert.NoError(t, err)
		assert.Equal(t, p, checkedPackageRepo)
	}
}

// TestShouldFailParsingInvalidName
// validates that an empty PackageRepo.Name fails IsValid
func TestShouldFailParsingInvalidName_PackageRepo(t *testing.T) {
	var checkedPackageRepo PackageRepo
	testPackageRepo := validPackageRepos[0]
	testPackageRepo.Name = ""

	err := testPackageRepo.nameIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for package repo name (), name cannot be empty", err.Error())

	err = remarshalJSON(testPackageRepo, &checkedPackageRepo)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [PackageRepo]: invalid value for package repo name (), name cannot be empty", err.Error())
}

// TestShouldFailParsingInvalidBaseUrl
// validates that an empty PackageRepo.BaseUrl fails IsValid
func TestShouldFailParsingInvalidBaseUrlEmptyString_PackageRepo(t *testing.T) {
	var checkedPackageRepo PackageRepo
	testPackageRepo := validPackageRepos[0]
	testPackageRepo.BaseUrl = ""

	err := testPackageRepo.repoUrlIsValid()
	assert.Error(t, err)
	assert.Equal(t, "invalid value for package repo URL (), URL cannot be empty", err.Error())

	err = remarshalJSON(testPackageRepo, &checkedPackageRepo)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [PackageRepo]: invalid value for package repo URL (), URL cannot be empty", err.Error())
}

// TestShouldFailParsingInvalidBaseUrl
// validates that a bogus URL fails IsValid
func TestShouldFailParsingInvalidBaseUrlBogusUrl_PackageRepo(t *testing.T) {
	var checkedPackageRepo PackageRepo
	testPackageRepo := validPackageRepos[0]
	testPackageRepo.BaseUrl = "asjhdjkshd"

	err := testPackageRepo.repoUrlIsValid()
	assert.Error(t, err)
	assert.Equal(t, "parse \"asjhdjkshd\": invalid URI for request", err.Error())

	err = remarshalJSON(testPackageRepo, &checkedPackageRepo)
	assert.Error(t, err)
	assert.Equal(t, "failed to parse [PackageRepo]: parse \"asjhdjkshd\": invalid URI for request", err.Error())
}

// TestShouldSucceedCreatingPackageRepoFile
// validates that package repo file can be created
func TestShouldSucceedCreatingPackageRepoFile_PackageRepo(t *testing.T) {
	curDir, err := os.Getwd()
	assert.NoError(t, err)
	testRepoFile := filepath.Join(curDir, "mariner-official-base.repo")
	testPackageRepo := validPackageRepos[0]

	err = createCustomPackageRepo(nil, testPackageRepo, curDir)
	assert.NoError(t, err)
	t.Cleanup(func() {
		os.Remove(testRepoFile)
	})

	testRepoContents, err := file.ReadLines(testRepoFile)
	assert.NoError(t, err)
	assert.Equal(t, testRepoContents, validRepoContent)
}

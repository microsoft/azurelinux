// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package repocloner

import "github.com/microsoft/CBL-Mariner/toolkit/tools/internal/pkgjson"

// RepoContents contains an array of packages contained in a repo.
type RepoContents struct {
	Repo []*RepoPackage `json:"Repo"`
}

// RepoPackage represents a package in a repo.
type RepoPackage struct {
	Name         string `json:"Name"`         // Name of the package
	Version      string `json:"Version"`      // Version number of the package
	Architecture string `json:"Architecture"` // Architecture of the package
	Distribution string `json:"Distribution"` // Distribution tag of the package
}

// RepoCloner is an interface for a package repository cloner.
// It is capable of generate a local repository consisting of a set of request packages
// and their dependencies.
type RepoCloner interface {
	AddNetworkFiles(tlsClientCert, tlsClientKey string) error
	BestProvidesCandidate(pkgVer *pkgjson.PackageVer) (packageName string, err error)
	Clone(cloneDeps bool, packagesToClone ...*pkgjson.PackageVer) (prebuiltPackage bool, err error)
	CloneDirectory() string
	ClonedRepoContents() (repoContents *RepoContents, err error)
	Close() error
	ConvertDownloadedPackagesIntoRepo() error
	Initialize(destinationDir, tmpDir, workerTar, existingRpmsDir string, usePreviewRepo bool, repoDefinitions []string) error
}

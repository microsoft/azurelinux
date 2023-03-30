// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package repomanager

// RepoManager is an interface for managing package repositories.
type RepoManager interface {
	// CreateRepo will create a package repository at repoDir
	CreateRepo(repoDir string) error

	// OrganizePackagesByArch will move packages in flatDir into architecture folders under repoDir
	OrganizePackagesByArch(flatDir, repoDir string) error
}

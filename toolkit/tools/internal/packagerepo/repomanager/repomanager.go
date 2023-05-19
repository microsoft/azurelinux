// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package repomanager

// RepoManager is an interface for managing package repositories.
type RepoManager interface {
	// CreateRepo will create a package repository at repoDir
	CreateRepo(repoDir string) error
	ValidateRpmPaths(repoDir string) error
}

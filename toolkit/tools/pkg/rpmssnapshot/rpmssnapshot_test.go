// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for generating snapshots of built RPMs from local specs.

package rpmssnapshot

import (
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/microsoft/azurelinux/toolkit/tools/internal/rpm"
	"github.com/stretchr/testify/assert"
)

func TestGenerateResults(t *testing.T) {
	input := []string{
		"pkg-1.2.3-1_2.3.azl3.x86_64",
		"other-pkg-1.2.3-1_2.3.azl3.x86_64",
		"ca-certificates-1:3.0.0-14.azl3.noarch",
	}
	expectedResults := repocloner.RepoContents{
		Repo: []*repocloner.RepoPackage{
			{
				Name:         "pkg",
				Version:      "1.2.3-1_2.3",
				Distribution: "azl3",
				Architecture: "x86_64",
			},
			{
				Name:         "other-pkg",
				Version:      "1.2.3-1_2.3",
				Distribution: "azl3",
				Architecture: "x86_64",
			},
			{
				Name:         "ca-certificates",
				Version:      "1:3.0.0-14",
				Distribution: "azl3",
				Architecture: "noarch",
			},
		},
	}
	emptySnapshotGenerator := SnapshotGenerator{}
	generatedContents, err := emptySnapshotGenerator.convertResultsToRepoContents(input)
	assert.NoError(t, err)
	assert.Equal(t, expectedResults, generatedContents)
}

func TestGenerateInvalidInput(t *testing.T) {
	input := []string{
		"pkg-no-version",
	}
	emptySnapshotGenerator := SnapshotGenerator{}
	_, err := emptySnapshotGenerator.convertResultsToRepoContents(input)
	assert.EqualError(t, err, "RPM package name ("+input[0]+") doesn't match the regular expression ("+rpm.RpmSpecBuiltRPMRegex.String()+")")
}

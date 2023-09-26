// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

// A tool for generating snapshots of built RPMs from local specs.

package rpmssnapshot

import (
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/packagerepo/repocloner"
	"github.com/stretchr/testify/assert"
)

func TestRegexBasic(t *testing.T) {
	input := "pkg-1.2.3-1.azl3.x86_64"
	expectedResults := []string{"pkg", "1.2.3-1", "azl3", "x86_64"}
	expectedMatchNumber := 5

	matches := rpmSpecBuiltRPMRegex.FindStringSubmatch(input)
	assert.Equal(t, expectedMatchNumber, len(matches))

	assert.Equal(t, expectedResults[0], matches[rpmSpecBuiltRPMRegexNameIndex])
	assert.Equal(t, expectedResults[1], matches[rpmSpecBuiltRPMRegexVersionIndex])
	assert.Equal(t, expectedResults[2], matches[rpmSpecBuiltRPMRegexDistributionIndex])
	assert.Equal(t, expectedResults[3], matches[rpmSpecBuiltRPMRegexArchitectureIndex])
}

func TestRegexUnderscore(t *testing.T) {
	input := "pkg-1.2.3-1_2.3.azl3.x86_64"
	expectedResults := []string{"pkg", "1.2.3-1_2.3", "azl3", "x86_64"}
	expectedMatchNumber := 5

	matches := rpmSpecBuiltRPMRegex.FindStringSubmatch(input)
	assert.Equal(t, expectedMatchNumber, len(matches))

	assert.Equal(t, expectedResults[0], matches[rpmSpecBuiltRPMRegexNameIndex])
	assert.Equal(t, expectedResults[1], matches[rpmSpecBuiltRPMRegexVersionIndex])
	assert.Equal(t, expectedResults[2], matches[rpmSpecBuiltRPMRegexDistributionIndex])
	assert.Equal(t, expectedResults[3], matches[rpmSpecBuiltRPMRegexArchitectureIndex])
}

func TestGenerateResults(t *testing.T) {
	input := []string{
		"pkg-1.2.3-1_2.3.azl3.x86_64",
		"other-pkg-1.2.3-1_2.3.azl3.x86_64",
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
	assert.EqualError(t, err, "RPM package name ("+input[0]+") doesn't match the regular expression ("+rpmSpecBuiltRPMRegex.String()+")")
}

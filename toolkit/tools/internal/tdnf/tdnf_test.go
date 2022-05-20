// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package tdnf

import (
	"os"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestGetMajorVersionFromString_AcceptEmptyMinorVersion(t *testing.T) {
	fullVersion := "2.0"
	expectedMajorVersion := "2.0"
	majorVersion, err := getMajorVersionFromString(fullVersion)

	assert.NoError(t, err)
	assert.Equal(t, expectedMajorVersion, majorVersion)
}

func TestGetMajorVersionFromString_AcceptPopulatedMinorVersionTimestamp(t *testing.T) {
	fullVersion := "2.0.20220519.1844"
	expectedMajorVersion := "2.0"
	majorVersion, err := getMajorVersionFromString(fullVersion)

	assert.NoError(t, err)
	assert.Equal(t, expectedMajorVersion, majorVersion)
}

func TestGetMajorVersionFromString_AcceptAlphabeticalMinorVersion(t *testing.T) {
	fullVersion := "2.0.reallycoolteststring"
	expectedMajorVersion := "2.0"
	majorVersion, err := getMajorVersionFromString(fullVersion)

	assert.NoError(t, err)
	assert.Equal(t, expectedMajorVersion, majorVersion)
}

func TestGetMajorVersionFromString_RejectAlphabeticalInMajor(t *testing.T) {
	fullVersion := "2.A"
	_, err := getMajorVersionFromString(fullVersion)
	assert.Error(t, err)
}

func TestGetMajorVersionFromString_RejectEmpty(t *testing.T) {
	fullVersion := ""
	_, err := getMajorVersionFromString(fullVersion)
	assert.Error(t, err)
}

func TestGetMajorVersionFromString_RejectWithNoDot(t *testing.T) {
	fullVersion := "2"
	_, err := getMajorVersionFromString(fullVersion)
	assert.Error(t, err)
}

func TestGetMajorVersionFromString_RejectNoSecondComponentWithDot(t *testing.T) {
	fullVersion := "2."
	_, err := getMajorVersionFromString(fullVersion)
	assert.Error(t, err)
}

func TestGetMajorVersionFromString_RejectTrailingDot(t *testing.T) {
	fullVersion := "2.0."
	_, err := getMajorVersionFromString(fullVersion)
	assert.Error(t, err)
}

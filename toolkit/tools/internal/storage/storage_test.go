// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package storage

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCheckDiskSpaceShouldReportDiskSpace(t *testing.T) {
	// Every disk should have at least 100kb to test
	err := CheckDiskSpace(".", 100)
	assert.NoError(t, err)
}

func TestCheckDiskSpaceShouldReportNoDiskSpace(t *testing.T) {
	// No disk should have more 1000TB
	err := CheckDiskSpace("/", 1000000000000)
	assert.Error(t, err)
}

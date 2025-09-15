// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package userutils

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestReadPasswdFile(t *testing.T) {
	expected := []PasswdEntry{
		{
			Name:          "root",
			Uid:           0,
			Gid:           0,
			Description:   "root",
			HomeDirectory: "/root",
			Shell:         "/bin/bash",
		},
		{
			Name:          "test",
			Uid:           1001,
			Gid:           100,
			Description:   "",
			HomeDirectory: "/home/1001",
			Shell:         "/bin/sh",
		},
	}

	entries, err := ReadPasswdFile(testDataDir)
	assert.NoError(t, err)
	assert.Equal(t, expected, entries)
}

func TestGetPasswdFileEntryForUser(t *testing.T) {
	expected := PasswdEntry{
		Name:          "test",
		Uid:           1001,
		Gid:           100,
		Description:   "",
		HomeDirectory: "/home/1001",
		Shell:         "/bin/sh",
	}

	entries, err := GetPasswdFileEntryForUser(testDataDir, "test")
	assert.NoError(t, err)
	assert.Equal(t, expected, entries)
}

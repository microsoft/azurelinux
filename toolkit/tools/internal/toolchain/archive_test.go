// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package toolchain

import (
	"fmt"
	"os"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
	"github.com/stretchr/testify/assert"
)

func TestMain(m *testing.M) {
	logger.InitStderrLog()
	os.Exit(m.Run())
}

func TestPrintManifestMissmatch(t *testing.T) {
	missingFromArchive := []string{"aPkg-v1"}
	missingFromManifest := []string{"aPkg-v2", "bPkg-v1"}
	archivePath := "archivePath"
	manifestPath := "manifestPath"

	expectedTableLines := []string{
		"Missmatched packages between:",
		"Archive: 'archivePath'",
		"Manifest: 'manifestPath'",
		"",
		"In Manifest Only",
		"\t\tIn Archive Only",
		"-----------------------",
		"aPkg-v1",
		"\t\taPkg-v2",
		"\t\tbPkg-v1",
		"",
	}

	tableLines := CreateManifestMissmatchReport(missingFromArchive, missingFromManifest, archivePath, manifestPath)

	assert.Equal(t, expectedTableLines, tableLines)

	for line := range tableLines {
		fmt.Println(tableLines[line])
	}
}

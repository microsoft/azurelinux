// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package imagecustomizerapi

import (
	"os"
	"testing"

	"github.com/microsoft/azurelinux/toolkit/tools/internal/logger"
)

var (
	workingDir string
)

func TestMain(m *testing.M) {
	var err error

	logger.InitStderrLog()

	workingDir, err = os.Getwd()
	if err != nil {
		logger.Log.Panicf("Failed to get working directory, error: %s", err)
	}

	retVal := m.Run()

	os.Exit(retVal)
}

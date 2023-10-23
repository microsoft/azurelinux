// Copyright (c) Microsoft Corporation.
// Licensed under the MIT License.

package userutils

import (
	"os"
	"path/filepath"
	"testing"

	"github.com/microsoft/CBL-Mariner/toolkit/tools/internal/logger"
)

var (
	tmpDir string
)

func TestMain(m *testing.M) {
	var err error

	logger.InitStderrLog()

	workingDir, err := os.Getwd()
	if err != nil {
		logger.Log.Panicf("Failed to get working directory, error: %s", err)
	}

	tmpDir = filepath.Join(workingDir, "_tmp")

	err = os.MkdirAll(tmpDir, os.ModePerm)
	if err != nil {
		logger.Log.Panicf("Failed to create tmp directory, error: %s", err)
	}

	retVal := m.Run()

	err = os.RemoveAll(tmpDir)
	if err != nil {
		logger.Log.Warnf("Failed to cleanup tmp dir (%s). Error: %s", tmpDir, err)
	}

	os.Exit(retVal)
}
